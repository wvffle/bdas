from gen import generate
import pprint
import subprocess
import time
import shutil
import os
import json


def execute_sqlite(input):
    result = subprocess.run(
        'sqlite3 sqlite.db', 
        input=input,
        shell=True,
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return result.stdout

def execute_mariadb(input):
    result = subprocess.run(
        'mysql --silent --socket=./mariadb_socket/mysqld.sock -u myuser -pmypassword mydatabase', 
        input=input,
        shell=True,
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return result.stdout

def execute_postgres(input):
    result = subprocess.run(
        'psql -q -h $(pwd)/postgresql_socket -U myuser -d mydatabase', 
        input=input,
        shell=True,
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return result.stdout

executors = {
    'sqlite': execute_sqlite,
    'mariadb': execute_mariadb,
    'postgresql': execute_postgres
}



# ===========================================
# Remove all of the tables from the databases
# ===========================================
print('Cleaning up databases...')
def cleanup_dbs():
    try:
        os.remove('sqlite.db')
    except Exception as e:
        pass

    execute_postgres("""
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
        GRANT ALL ON SCHEMA public TO myuser;
        GRANT ALL ON SCHEMA public TO public;
    """)

    with open('cleanup-mariadb.sql', 'r') as f:
        execute_mariadb(f.read())
    

stats = {
    'sqlite': {},
    'sqlite-optimized': {},
    'mariadb': {},
    'postgresql': {}
}

for n in [1, 100, 2000, 4000, 8000, 20000]:
    for x in stats.keys():
        stats[x][n] = {}

def run_test(backend, i=1, optimized=False):
    execute = executors[backend]
    stats_entry = backend

    if backend == 'sqlite':
        if optimized:
            stats_entry += '-optimized'

    with os.scandir('data') as entries:
        for entry in entries:
            if not entry.is_dir():
                continue

            print(f'[{stats_entry}][{n}][{i}/10] {entry.name}')
            if entry.name not in stats[stats_entry][n]:
                stats[stats_entry][n][entry.name] = []

            with open(f'{entry.path}/{backend}.sql', 'r') as f:
                data = f.read()

                if backend == 'sqlite':
                    if optimized:
                        data = """
                        PRAGMA journal_mode = WAL;
                        PRAGMA synchronous = NORMAL;
                        PRAGMA temp_store = MEMORY;
                        """ + data
                    else:
                        data = """
                        PRAGMA journal_mode = DELETE;
                        PRAGMA synchronous = FULL;
                        PRAGMA temp_store = DEFAULT;
                        """ + data

                then = time.time_ns()
                execute(data)
                delta = time.time_ns() - then
                stats[stats_entry][n][entry.name].append(delta)

n = 1
def main():
    global n
    for n in [1, 100, 2000, 4000, 8000, 20000]:
        print('Generating SQL data...')
        print(f'n = {n}')
        generate(n)

        print('Running tests...')
        for i in range(10):
            print(f'Iteration {i+1}/10')

            # Enable optimized for SQLite
            cleanup_dbs()
            run_test('sqlite', i=i, optimized=True)

            # Run for other backends
            cleanup_dbs()
            for backend in executors.keys():
                run_test(backend, i=i)

        print('')

    shutil.rmtree('out')
    os.makedirs('out', exist_ok=True)

    with open('out/stats.json', 'w') as f:
        json.dump(stats, f)

    backends = list(stats.keys())
    values = {}
    for backend in stats.keys():
        for n in stats[backend].keys():
            tests = stats[backend][n]

            for test in tests.keys():
                if test not in values:
                    values[test] = {}

                if n not in values[test]:
                    values[test][n] = []

                values[test][n].append(sum(tests[test]) / len(tests[test]))

    import matplotlib.pyplot as plt
    for test in values.keys():
        fig, axs = plt.subplots(2, 3, figsize=(20, 10))
        axs = axs.flatten()

        for i, n in enumerate(values[test].keys()):
            axs[i].bar(backends, values[test][n])
            axs[i].set_title(f'{test} (n = {n})')
            axs[i].set_ylabel('Avg. Time (ns)')
            axs[i].set_xlabel('Database Backend')

        plt.tight_layout()
        plt.savefig(f'out/{test}.png')

main()

from faker import Faker
import random
import datetime
import shutil
import os

most_common_word = 'common'

def generate(n):
    # Initialize Faker
    fake = Faker()

    def test(directory, fn):
        os.makedirs(directory, exist_ok=True)
        with open(f'{directory}/sqlite.sql', 'w') as f:
            fn(f)
        shutil.copyfile(f'{directory}/sqlite.sql', f'{directory}/mariadb.sql')
        shutil.copyfile(f'{directory}/sqlite.sql', f'{directory}/postgresql.sql')



    with os.scandir('data') as entries:
        for entry in entries:
            if entry.is_dir():
                if entry.name == '01-create-db':
                    continue

                shutil.rmtree(entry.path)

    # ======================================
    # Seed data
    # ======================================
    def f(f):
        f.write("-- Wydazenia\n")
        f.write(f"INSERT INTO Wydarzenie (nazwa, data_od, data_do, data_dodania, data_edycji, data_usuniecia)\nVALUES\n")

        names = []
        for i in range(n):
            nazwa = fake.catch_phrase()
            names.append(nazwa)

            data_od = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            data_do = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            data_dodania = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            data_edycji = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            data_usuniecia = fake.date_time_between(start_date='now', end_date='+2y').strftime('%Y-%m-%d %H:%M:%S')
            endchar = ',' if i < n - 1 else ''
            f.write(f"  ('{nazwa}', '{data_od}', '{data_do}', '{data_dodania}', '{data_edycji}', '{data_usuniecia}'){endchar}\n")
        f.write(";")

        # Get most common word from list of names
        all_words = ' '.join(names).split(' ')
        from collections import Counter

        global most_common_word
        most_common_word = Counter(all_words).most_common(1)[0][0]
        
        f.write("\n\n-- Gry\n")
        f.write(f"INSERT INTO Gra (nazwa, kod_qr, waga, ilosc_sztuk, data_edycji)\nVALUES\n")
        for i in range(n):
            nazwa = fake.company()
            kod_qr = fake.uuid4()
            waga = round(random.uniform(0.1, 10.0), 2)
            ilosc_sztuk = random.randint(1, 100)
            data_edycji = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            endchar = ',' if i < n - 1 else ''
            f.write(f"  ('{nazwa}', '{kod_qr}', {waga}, {ilosc_sztuk}, '{data_edycji}'){endchar}\n")
        f.write(";")
        
        f.write("\n\n-- Zdjęcia\n")
        f.write(f"INSERT INTO Zdjecie (id_gry, dane, data_dodania)\nVALUES\n")
        for i in range(n):
            id_gry = random.randint(1, n)
            dane = fake.image_url()
            data_dodania = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            endchar = ',' if i < n - 1 else ''
            f.write(f"  ({id_gry}, '{dane}', '{data_dodania}'){endchar}\n")
        f.write(";")

        f.write("\n\n-- Klienci\n")
        f.write("INSERT INTO Klient (numer_karty, imie_i_nazwisko, numer_telefonu, data_dodania, data_edycji, data_usuniecia)\nVALUES\n")
        for i in range(n):
            numer_karty = fake.credit_card_number()
            imie_i_nazwisko = fake.name()
            numer_telefonu = fake.phone_number()
            data_dodania = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            data_edycji = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            data_usuniecia = fake.date_time_between(start_date='now', end_date='+2y').strftime('%Y-%m-%d %H:%M:%S')
            endchar = ',' if i < n - 1 else ''
            f.write(f"  ('{numer_karty}', '{imie_i_nazwisko}', '{numer_telefonu}', '{data_dodania}', '{data_edycji}', '{data_usuniecia}'){endchar}\n")
        f.write(";")

    test('data/02-seed', f)

    # ======================================
    # Batch insert
    # ======================================
    def f(f):
        f.write("\n\n-- Wypożyczenia\n")
        f.write("INSERT INTO Wypozyczenie (id_gry, id_klienta, id_eventu, data_oddania, data_dodania, data_edycji, data_usuniecia)\nVALUES\n")
        for i in range(n):
            id_gry = random.randint(1, n)
            id_klienta = random.randint(1, n)
            id_eventu = random.randint(1, n)
            data_oddania = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            data_dodania = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            data_edycji = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            data_usuniecia = fake.date_time_between(start_date='now', end_date='+2y').strftime('%Y-%m-%d %H:%M:%S')
            endchar = ',' if i < n - 1 else ''
            f.write(f"    ({id_gry}, {id_klienta}, {id_eventu}, '{data_oddania}', '{data_dodania}', '{data_edycji}', '{data_usuniecia}'){endchar}\n")
        f.write(";")

    test('data/03-insert-batch', f)


    # ======================================
    # Update All
    # ======================================

    def f(f):
        f.write("UPDATE Wypozyczenie SET data_usuniecia = NULL, data_oddania = NULL;")

    test('data/06-update-all', f)

    # ======================================
    # Update half with WHERE clause
    # ======================================

    def f(f):
        f.write("UPDATE Wypozyczenie SET data_oddania = CURRENT_DATE WHERE id % 2 = 0;")

    test('data/07-update-half', f)


    # ======================================
    # Select simple query
    # ======================================

    def f(f):
        f.write(f"""
            SELECT * FROM Wypozyczenie;
        """)

    test('data/08-select-all', f)

    # ======================================
    # Select with join
    # ======================================

    def f(f):
        f.write(f"""
            SELECT Gra.nazwa AS nazwa_gry, Klient.imie_i_nazwisko AS imie_i_nazwisko_klienta, Wydarzenie.nazwa AS nazwa_wydarzenia
            FROM Wypozyczenie
            INNER JOIN Gra ON Wypozyczenie.id_gry = Gra.id
            INNER JOIN Klient ON Wypozyczenie.id_klienta = Klient.id
            INNER JOIN Wydarzenie ON Wypozyczenie.id_eventu = Wydarzenie.id;
        """)

    test('data/09-select-with-join', f)


    # ======================================
    # Select complex query
    # ======================================

    def f(f):
        f.write(f"""
            SELECT Gra.nazwa AS nazwa_gry, COUNT(Wypozyczenie.id) AS liczba_wypozyczen
            FROM Wypozyczenie
            INNER JOIN Gra ON Wypozyczenie.id_gry = Gra.id
            WHERE id_gry IN (SELECT id FROM Gra WHERE waga > 2.0)
            AND id_klienta IN (SELECT id FROM Klient WHERE numer_telefonu LIKE '%8%')
            AND id_eventu IN (SELECT id FROM Wydarzenie WHERE nazwa LIKE '%{most_common_word}%')
            GROUP BY Gra.nazwa;
        """)

    test('data/10-select-complex-query', f)

    # ======================================
    # Delete all at once
    # ======================================

    def f(f):
        f.write("DELETE FROM Wypozyczenie;\n")

    test('data/11-delete-all', f)

    # ======================================
    # One insert per line
    # ======================================

    #def f(f):
    #    f.write("\n\n-- Wypożyczenia\n")
    #    for _ in range(n):
    #        id_gry = random.randint(1, n)
    #        id_klienta = random.randint(1, n)
    #        id_eventu = random.randint(1, n)
    #        data_oddania = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
    #        data_dodania = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
    #        data_edycji = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
    #        data_usuniecia = fake.date_time_between(start_date='now', end_date='+2y').strftime('%Y-%m-%d %H:%M:%S')
    #        f.write("INSERT INTO Wypozyczenie (id_gry, id_klienta, id_eventu, data_oddania, data_dodania, data_edycji, data_usuniecia)\nVALUES\n")
    #        f.write(f"    ({id_gry}, {id_klienta}, {id_eventu}, '{data_oddania}', '{data_dodania}', '{data_edycji}', '{data_usuniecia}');")
    #test('data/12-insert-one-per-line', f)

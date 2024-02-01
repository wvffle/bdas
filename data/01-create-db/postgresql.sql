-- Gra
CREATE TABLE Gra (
    id SERIAL PRIMARY KEY,
    nazwa VARCHAR(255),
    kod_qr UUID,
    waga REAL,
    ilosc_sztuk INTEGER,
    data_edycji TIMESTAMP
);

-- Zdjecie
CREATE TABLE Zdjecie (
    id SERIAL PRIMARY KEY,
    id_gry INTEGER,
    dane VARCHAR(255),
    data_dodania TIMESTAMP
);

-- Klient
CREATE TABLE Klient (
    id SERIAL PRIMARY KEY,
    numer_karty VARCHAR(255) UNIQUE,
    imie_i_nazwisko VARCHAR(255),
    numer_telefonu VARCHAR(255),
    data_dodania TIMESTAMP,
    data_edycji TIMESTAMP,
    data_usuniecia TIMESTAMP
);

-- Wydarzenie
CREATE TABLE Wydarzenie (
    id SERIAL PRIMARY KEY,
    nazwa VARCHAR(255),
    data_od TIMESTAMP,
    data_do TIMESTAMP,
    data_dodania TIMESTAMP,
    data_edycji TIMESTAMP,
    data_usuniecia TIMESTAMP
);

-- Wypozyczenie
CREATE TABLE Wypozyczenie (
    id SERIAL PRIMARY KEY,
    id_gry INTEGER,
    id_klienta INTEGER,
    id_eventu INTEGER,
    data_oddania TIMESTAMP,
    data_dodania TIMESTAMP,
    data_edycji TIMESTAMP,
    data_usuniecia TIMESTAMP
);

-- Gra
CREATE TABLE Gra (
    id INTEGER PRIMARY KEY,
    nazwa TEXT,
    kod_qr TEXT,
    waga FLOAT,
    ilosc_sztuk INTEGER,
    data_edycji TEXT
);

-- Zdjecie
CREATE TABLE Zdjecie (
    id INTEGER PRIMARY KEY,
    id_gry INTEGER,
    dane TEXT,
    data_dodania TEXT
);

-- Klient
CREATE TABLE Klient (
    id INTEGER PRIMARY KEY,
    numer_karty TEXT UNIQUE,
    imie_i_nazwisko TEXT,
    numer_telefonu TEXT,
    data_dodania TEXT,
    data_edycji TEXT,
    data_usuniecia TEXT
);

-- Wydarzenie
CREATE TABLE Wydarzenie (
    id INTEGER PRIMARY KEY,
    nazwa TEXT,
    data_od TEXT,
    data_do TEXT,
    data_dodania TEXT,
    data_edycji TEXT,
    data_usuniecia TEXT
);

-- Wypozyczenie
CREATE TABLE Wypozyczenie (
    id INTEGER PRIMARY KEY,
    id_gry INTEGER,
    id_klienta INTEGER,
    id_eventu INTEGER,
    data_oddania TEXT,
    data_dodania TEXT,
    data_edycji TEXT,
    data_usuniecia TEXT
);

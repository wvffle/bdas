-- Gra
CREATE TABLE Gra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazwa VARCHAR(255),
    kod_qr VARCHAR(255),
    waga FLOAT,
    ilosc_sztuk INT,
    data_edycji DATETIME
);

-- Zdjecie
CREATE TABLE Zdjecie (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_gry INT,
    dane VARCHAR(255),
    data_dodania DATETIME
);

-- Klient
CREATE TABLE Klient (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numer_karty VARCHAR(255) UNIQUE,
    imie_i_nazwisko VARCHAR(255),
    numer_telefonu VARCHAR(255),
    data_dodania DATETIME,
    data_edycji DATETIME,
    data_usuniecia DATETIME
);

-- Wydarzenie
CREATE TABLE Wydarzenie (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazwa VARCHAR(255),
    data_od DATETIME,
    data_do DATETIME,
    data_dodania DATETIME,
    data_edycji DATETIME,
    data_usuniecia DATETIME
);

-- Wypozyczenie
CREATE TABLE Wypozyczenie (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_gry INT,
    id_klienta INT,
    id_eventu INT,
    data_oddania DATETIME,
    data_dodania DATETIME,
    data_edycji DATETIME,
    data_usuniecia DATETIME
);

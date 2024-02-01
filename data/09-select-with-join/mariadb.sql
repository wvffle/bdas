
            SELECT Gra.nazwa AS nazwa_gry, Klient.imie_i_nazwisko AS imie_i_nazwisko_klienta, Wydarzenie.nazwa AS nazwa_wydarzenia
            FROM Wypozyczenie
            INNER JOIN Gra ON Wypozyczenie.id_gry = Gra.id
            INNER JOIN Klient ON Wypozyczenie.id_klienta = Klient.id
            INNER JOIN Wydarzenie ON Wypozyczenie.id_eventu = Wydarzenie.id;
        
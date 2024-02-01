
            SELECT Gra.nazwa AS nazwa_gry, COUNT(Wypozyczenie.id) AS liczba_wypozyczen
            FROM Wypozyczenie
            INNER JOIN Gra ON Wypozyczenie.id_gry = Gra.id
            WHERE id_gry IN (SELECT id FROM Gra WHERE waga > 2.0)
            AND id_klienta IN (SELECT id FROM Klient WHERE numer_telefonu LIKE '%8%')
            AND id_eventu IN (SELECT id FROM Wydarzenie WHERE nazwa LIKE '%zero%')
            GROUP BY Gra.nazwa;
        
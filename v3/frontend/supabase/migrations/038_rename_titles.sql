-- Rename Modules
UPDATE modules SET title = 'FUNDAMENTY MILWAUKEE' WHERE title LIKE 'Milwaukee Foundations%';
UPDATE modules SET title = 'APPLICATION FIRST – METODA DIAGNOZY APLIKACJI' WHERE title LIKE 'Application First Canvas%';
UPDATE modules SET title = 'STANDARD WIZYTY JSS – RAMY ROZMOWY' WHERE title LIKE 'Standard Wizyty%';
UPDATE modules SET title = 'WSPÓŁPRACA W MODELU ONE MILWAUKEE' WHERE title LIKE 'Współpraca%';

-- Rename Lessons - Module 1: Fundamenty
UPDATE lessons SET title = 'Historia i DNA marki Milwaukee – Nothing but HEAVY DUTY™' WHERE title ILIKE '%Milwaukee Story%';
UPDATE lessons SET title = 'Portfolio Milwaukee – myślenie systemowe, nie produktowe' WHERE title ILIKE '%Portfolio%';
UPDATE lessons SET title = 'Application First – jak myślimy o pracy klienta' WHERE title ILIKE '%Application First - Filozofia%';
UPDATE lessons SET title = 'System Milwaukee – cztery elementy rozwiązania' WHERE title ILIKE '%SYSTEM Milwaukee%';
UPDATE lessons SET title = 'Rynek i konkurencja – obiektywne porównanie' WHERE title ILIKE '%Competition%';
UPDATE lessons SET title = 'Język i komunikacja Milwaukee' WHERE title ILIKE '%Branding%';

-- Rename Lessons - Module 2: Application First (Kroki)
UPDATE lessons SET title = 'Krok 1: Aplikacja – co klient naprawdę robi' WHERE title ILIKE '%KROK 1%' OR title ILIKE '%Job to be Done%';
UPDATE lessons SET title = 'Krok 2: Problem – co dziś nie działa' WHERE title ILIKE '%KROK 2%' OR title ILIKE '%Pain Points%';
UPDATE lessons SET title = 'Krok 3: Konsekwencje – jakie są straty i ryzyka' WHERE title ILIKE '%KROK 3%' OR title ILIKE '%Impact%';
UPDATE lessons SET title = 'Krok 4: Rozwiązanie – system dopasowany do aplikacji' WHERE title ILIKE '%KROK 4%' OR title ILIKE '%SYSTEM)%';
UPDATE lessons SET title = 'Krok 5: Demo aplikacyjne – dowód w praktyce' WHERE title ILIKE '%KROK 5%' OR title ILIKE '%Proof%';
UPDATE lessons SET title = 'Krok 6: Wartość – co klient realnie zyskuje' WHERE title ILIKE '%KROK 6%' OR title ILIKE '%Value%';
UPDATE lessons SET title = 'Krok 7: Kolejne kroki – decyzje i odpowiedzialności' WHERE title ILIKE '%KROK 7%' OR title ILIKE '%Domknięcie%';

-- Rename Lessons - Module 3: Standard Wizyty
UPDATE lessons SET title = 'Przygotowanie do wizyty – cel, kontekst, plan' WHERE title ILIKE '%Przygotowanie do Wizyty%';
UPDATE lessons SET title = 'Otwarcie wizyty i budowanie relacji' WHERE title ILIKE '%Otwarcie Wizyty%';
UPDATE lessons SET title = 'Rozpoznanie potrzeb – zadawanie pytań i słuchanie' WHERE title ILIKE '%Discovery%';
UPDATE lessons SET title = 'Prowadzenie rozmowy – logika i struktura wizyty' WHERE title ILIKE '%Prowadzenie Rozmowy%';
UPDATE lessons SET title = 'Prezentowanie rozwiązań w sposób przekonujący' WHERE title ILIKE '%jak prezentować%';
UPDATE lessons SET title = 'Praca z obiekcjami klienta' WHERE title ILIKE '%Handling%';
UPDATE lessons SET title = 'Ustalenie decyzji i kolejnych kroków' WHERE title ILIKE '%Closing & Next Steps%';
UPDATE lessons SET title = 'Podsumowanie wizyty i praca w CRM' WHERE title ILIKE '%CRM Documentation%';

-- Rename Lessons - Module 4: Współpraca
UPDATE lessons SET title = 'Współpraca JSS i ASR w terenie' WHERE title ILIKE '%JSS ↔ ASR%';
UPDATE lessons SET title = 'Ścieżka klienta – sell-out i sell-in w praktyce' WHERE title ILIKE '%Sell-In%';
UPDATE lessons SET title = 'Cross-selling – dobre praktyki' WHERE title ILIKE '%Cross%';
UPDATE lessons SET title = 'Współpraca z marketingiem – wsparcie i informacja zwrotna' WHERE title ILIKE '%Współpraca z Marketingiem%';
UPDATE lessons SET title = 'Obsługa posprzedażowa i wsparcie klienta' WHERE title ILIKE '%Aftersales%';

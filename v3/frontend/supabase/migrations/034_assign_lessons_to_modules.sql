-- Helper function/logic to assign module_id based on lesson titles

-- Module 1: Milwaukee Foundations
UPDATE lessons 
SET module_id = (SELECT id FROM modules WHERE title = 'Milwaukee Foundations' LIMIT 1),
    track = 'associate'
WHERE title ILIKE '%Milwaukee Story%'
   OR title ILIKE '%Portfolio Overview%'
   OR title ILIKE '%Filozofia Pracy%'
   OR title ILIKE '%SYSTEM Milwaukee%'
   OR title ILIKE '%Competition Landscape%'
   OR title ILIKE '%Branding & Communication%';

-- Module 2: Application First Canvas (Now Module 2)
UPDATE lessons 
SET module_id = (SELECT id FROM modules WHERE title ILIKE 'Application First Canvas%' LIMIT 1),
    track = 'associate'
WHERE title ILIKE '%KROK 1%'
   OR title ILIKE '%KROK 2%'
   OR title ILIKE '%KROK 3%'
   OR title ILIKE '%KROK 4%'
   OR title ILIKE '%KROK 5%'
   OR title ILIKE '%KROK 6%'
   OR title ILIKE '%KROK 7%';

-- Module 3: Standard Wizyty "One Milwaukee" (Now Module 3)
UPDATE lessons 
SET module_id = (SELECT id FROM modules WHERE title ILIKE 'Standard Wizyty%' LIMIT 1),
    track = 'associate'
WHERE title ILIKE '%Przygotowanie do Wizyty%'
   OR title ILIKE '%Otwarcie Wizyty%'
   OR title ILIKE '%Building Rapport%'
   OR title ILIKE '%Discovery%'
   OR title ILIKE '%Diagnoza%'
   OR title ILIKE '%Prowadzenie Rozmowy%'
   OR title ILIKE '%Presentation Skills%'
   OR title ILIKE '%Handling Objections%'
   OR title ILIKE '%Closing%'
   OR title ILIKE '%Follow-Up%';

-- Module 4: Współpraca & One Milwaukee
UPDATE lessons 
SET module_id = (SELECT id FROM modules WHERE title ILIKE 'Współpraca%' LIMIT 1),
    track = 'associate'
WHERE title ILIKE '%JSS ↔ ASR%'
   OR title ILIKE '%Sell-In ↔ Sell-Out%'
   OR title ILIKE '%Cross-Sell%'
   OR title ILIKE '%Współpraca z Marketingiem%'
   OR title ILIKE '%Współpraca z Aftersales%';

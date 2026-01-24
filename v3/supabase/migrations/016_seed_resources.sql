-- Migration: 016_seed_resources.sql
-- Description: Seed initial resources data
-- Author: BrainVenture V3
-- Date: 2026-01-23

-- Clear existing resources to avoid duplicates during dev
TRUNCATE resources CASCADE;

-- 1. Sales Resources
INSERT INTO resources (resource_id, title, description, resource_type, category, content, image_url, download_xp, tier, external_url)
VALUES 
(
    'res-obiekcje-pdf',
    'Najczęstsze Obiekcje Klienta',
    'Kompletny przewodnik jak radzić sobie z 10 najtrudniejszymi obiekcjami. Gotowe scenariusze odpowiedzi.',
    'pdf',
    'Sprzedaż',
    '{"file_path": "/assets/docs/obiekcje_2025.pdf"}'::jsonb,
    'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&q=80&w=600',
    20,
    1,
    '#'
),
(
    'res-spin-questions',
    'Lista Pytań SPIN',
    '50 gotowych pytań do każdej fazy metody SPIN (Situation, Problem, Implication, Need-payoff).',
    'guide',
    'Sprzedaż',
    '{"file_path": "/assets/docs/spin_questions.pdf"}'::jsonb,
    'https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&q=80&w=600',
    15,
    1,
    '#'
);

-- 2. Product Knowledge
INSERT INTO resources (resource_id, title, description, resource_type, category, content, image_url, download_xp, tier, external_url)
VALUES 
(
    'res-katalog-ppe-2025',
    'Katalog PPE 2025',
    'Pełny katalog środków ochrony indywidualnej Milwaukee na rok 2025.',
    'pdf',
    'Wiedza produktowa',
    '{"file_path": "#"}'::jsonb,
    'https://images.unsplash.com/photo-1581092921461-eab6245b0a62?auto=format&fit=crop&q=80&w=600',
    50,
    1,
    'https://s3.eu-west-2.amazonaws.com/milwaukee-poland/MILWAUKEE_PPE_Catalogue_2025-PL.pdf'
),
(
    'res-m12-vs-m18',
    'M12 vs M18 - Porównanie',
    'Tabela szybkiego doboru platformy. Kiedy wybrać M12, a kiedy M18? Idealne do pokazania klientowi.',
    'table',
    'Wiedza produktowa',
    '{"file_path": "/assets/docs/comparison_m12_m18.pdf"}'::jsonb,
    'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?auto=format&fit=crop&q=80&w=600',
    10,
    1,
    '#'
);

-- 3. Tools / Calculators
INSERT INTO resources (resource_id, title, description, resource_type, category, content, image_url, download_xp, tier, external_url)
VALUES 
(
    'res-calc-marza',
    'Kalkulator Marży i Narzutu',
    'Prosty arkusz Excel do szybkiego obliczania marży, narzutu i ROI dla klienta.',
    'template',
    'Narzędzia',
    '{"file_path": "/assets/tools/margin_calc.xlsx"}'::jsonb,
    'https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&q=80&w=600',
    25,
    1,
    '#'
),
(
    'res-roi-calculator',
    'Kalkulator ROI Narzędzi',
    'Pokaż klientowi ile zaoszczędzi kupując narzędzia akumulatorowe vs tradycyjne.',
    'tool',
    'Narzędzia',
    '{"file_path": "/assets/tools/roi_calc.xlsx"}'::jsonb,
    'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=600',
    30,
    2,
    '#'
),
(
    'res-margin-calculator',
    'Kalkulator Marży (GP) Excel',
    'Szybko przelicz narzut na marżę i odwrotnie. Niezbędne przy negocjacjach.',
    'tool',
    'Narzędzia',
    '{"file_path": "/assets/tools/margin_calc.xlsx"}'::jsonb,
    'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&q=80&w=600',
    30,
    1,
    '#'
);

-- 4. Templates
INSERT INTO resources (resource_id, title, description, resource_type, category, content, image_url, download_xp, tier, external_url)
VALUES 
(
    'res-oferta-handlowa',
    'Szablon Oferty Handlowej',
    'Profesjonalny wzór oferty w Word. Wystarczy podmienić logo i produkty.',
    'template',
    'Organizacja',
    '{"file_path": "/assets/templates/offer_template_v2.docx"}'::jsonb,
    'https://images.unsplash.com/photo-1586281380349-632531db7ed4?auto=format&fit=crop&q=80&w=600',
    40,
    2,
    '#'
),
(
    'res-plan-wizyty',
    'Checklista Planowania Wizyty',
    'Lista 10 punktów do sprawdzenia przed wyjściem do klienta. Nie zapomnij o niczym.',
    'pdf',
    'Organizacja',
    '{"file_path": "/assets/docs/checklist_visit.pdf"}'::jsonb,
    'https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?auto=format&fit=crop&q=80&w=600',
    15,
    1,
    '#'
);

-- 5. Leadership (Locked example)
INSERT INTO resources (resource_id, title, description, resource_type, category, content, image_url, download_xp, tier, locked, external_url)
VALUES 
(
    'res-leadership-guide',
    'Przywództwo dla Area Managera',
    'Zaawansowane techniki zarządzania regionem i zespołem. Tylko dla poziomu Senior.',
    'ebook',
    'Leadership',
    '{"file_path": "/assets/docs/leadership_masterclass.pdf"}'::jsonb,
    'https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&q=80&w=600',
    100,
    3,
    true,
    '#'
);

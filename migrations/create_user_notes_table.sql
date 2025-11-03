-- Migration: Create user_notes table
-- Date: 2025-11-02
-- Description: Tabela do przechowywania notatek gracza (produkty, pitches, klienci, feedback)

CREATE TABLE IF NOT EXISTS user_notes (
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    
    -- Kategoria notatki
    category TEXT NOT NULL CHECK(category IN (
        'product_card',      -- Karta produktu (cena, marża, USP)
        'elevator_pitch',    -- Elevator pitches
        'mentor_tip',        -- Wskazówki od mentora
        'manager_feedback',  -- Feedback od menedżera
        'client_profile',    -- Profil klienta (osobowość, historia)
        'personal'           -- Notatki własne gracza
    )),
    
    -- Treść notatki
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    
    -- Relacje (opcjonalne)
    related_product_id INTEGER DEFAULT NULL,  -- FK do products.product_id
    related_client_id INTEGER DEFAULT NULL,   -- FK do clients.client_id
    
    -- Organizacja
    is_pinned BOOLEAN DEFAULT 0,              -- Przypięta notatka (na górze)
    color_tag TEXT DEFAULT NULL,              -- Opcjonalny tag kolorystyczny
    tags TEXT DEFAULT NULL,                   -- JSON array tagów (np. '["premium", "marża"]')
    
    -- Metadane
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign keys
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Indeksy dla wydajności
CREATE INDEX IF NOT EXISTS idx_notes_user ON user_notes(user_id);
CREATE INDEX IF NOT EXISTS idx_notes_category ON user_notes(category);
CREATE INDEX IF NOT EXISTS idx_notes_pinned ON user_notes(is_pinned);
CREATE INDEX IF NOT EXISTS idx_notes_product ON user_notes(related_product_id);
CREATE INDEX IF NOT EXISTS idx_notes_client ON user_notes(related_client_id);

-- Trigger do automatycznej aktualizacji updated_at
CREATE TRIGGER IF NOT EXISTS update_notes_timestamp 
AFTER UPDATE ON user_notes
BEGIN
    UPDATE user_notes SET updated_at = CURRENT_TIMESTAMP
    WHERE note_id = NEW.note_id;
END;

-- Przykładowe dane testowe (opcjonalne - zakomentowane)
/*
INSERT INTO user_notes (user_id, category, title, content, is_pinned, tags) VALUES
(1, 'product_card', 'Chocolate Supreme', 
 'Cena hurtowa: €15.20 (sugerowana: €17.99)\nMarża: 35%\nUSP: Premium kakao z Ghany, Fair Trade\nKonkurencja: Tańszy o €2 od Brand X',
 1, '["czekolada", "premium", "fairtrade"]'),

(1, 'elevator_pitch', 'Pitch dla produktów premium',
 'Nasze produkty premium to nie tylko najwyższa jakość składników, ale przede wszystkim marża 30-35% i lojalność klientów. W podobnych sklepach sprzedaż wzrosła o 40% po wprowadzeniu naszej linii premium.',
 1, '["premium", "marża"]'),

(1, 'client_profile', 'Supermarket ABC - Pan Kowalski',
 'Typ osobowości: ISTJ (faktyczny, systematyczny)\nPreferencje: Produkty lokalne, certyfikaty BIO\nPain points: Problemy z dostawami\nHistoria: 3x zamówienia premium w Q3 2025',
 1, '["supermarket", "ISTJ"]');
*/

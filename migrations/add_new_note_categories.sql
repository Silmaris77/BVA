-- Migration: Add new note categories (visit_ideas, market_analysis, training_notes)
-- Date: 2025-11-06
-- Description: Rozszerzenie kategorii notatek o nowe typy dla gry FMCG

-- SQLite nie pozwala modyfikować CHECK constraint bezpośrednio
-- Musimy:
-- 1. Utworzyć nową tabelę z rozszerzonym constraint
-- 2. Skopiować dane
-- 3. Usunąć starą tabelę
-- 4. Zmienić nazwę nowej tabeli

BEGIN TRANSACTION;

-- 1. Utwórz nową tabelę z rozszerzonymi kategoriami
CREATE TABLE IF NOT EXISTS user_notes_new (
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    
    -- Kategoria notatki - ROZSZERZONE
    category TEXT NOT NULL CHECK(category IN (
        'product_card',      -- Karta produktu (cena, marża, USP)
        'elevator_pitch',    -- Elevator pitches
        'mentor_tip',        -- Wskazówki od mentora
        'manager_feedback',  -- Feedback od menedżera
        'client_profile',    -- Profil klienta (osobowość, historia)
        'personal',          -- Notatki własne gracza
        'visit_ideas',       -- Pomysły na wizyty (NOWE)
        'market_analysis',   -- Analiza rynku/konkurencji (NOWE)
        'training_notes'     -- Notatki ze szkoleń (NOWE)
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

-- 2. Skopiuj wszystkie dane ze starej tabeli
INSERT INTO user_notes_new 
SELECT * FROM user_notes;

-- 3. Usuń starą tabelę
DROP TABLE user_notes;

-- 4. Zmień nazwę nowej tabeli
ALTER TABLE user_notes_new RENAME TO user_notes;

-- 5. Odtwórz indeksy
CREATE INDEX IF NOT EXISTS idx_notes_user ON user_notes(user_id);
CREATE INDEX IF NOT EXISTS idx_notes_category ON user_notes(category);
CREATE INDEX IF NOT EXISTS idx_notes_pinned ON user_notes(is_pinned);
CREATE INDEX IF NOT EXISTS idx_notes_product ON user_notes(related_product_id);
CREATE INDEX IF NOT EXISTS idx_notes_client ON user_notes(related_client_id);

-- 6. Odtwórz trigger
CREATE TRIGGER IF NOT EXISTS update_notes_timestamp 
AFTER UPDATE ON user_notes
BEGIN
    UPDATE user_notes SET updated_at = CURRENT_TIMESTAMP
    WHERE note_id = NEW.note_id;
END;

COMMIT;

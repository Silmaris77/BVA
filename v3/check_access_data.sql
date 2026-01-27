-- Sprawdź ID firmy 'Szkoła' i roli 'Uczeń'
SELECT id, company_slug, name FROM companies WHERE name ILIKE '%Szkoła%' OR company_slug ILIKE '%szkola%';
SELECT id, role_slug, display_name FROM user_roles WHERE display_name ILIKE '%Uczeń%' OR role_slug ILIKE '%uczen%';

-- Pobierz lekcje ze ścieżki "Matematyka - 7 klasa"
-- W insert_math_path.sql slug ścieżki to 'math-grade-7'
SELECT lesson_sequence FROM learning_paths WHERE title = 'Matematyka - 7 klasa';

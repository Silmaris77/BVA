-- 1. Sets 'Application First Canvas' to order 2
UPDATE modules
SET display_order = 2
WHERE title = 'Application First Canvas';

-- 2. Sets 'Standard Wizyty "One Milwaukee"' to order 3
UPDATE modules
SET display_order = 3
WHERE title = 'Standard Wizyty "One Milwaukee"';

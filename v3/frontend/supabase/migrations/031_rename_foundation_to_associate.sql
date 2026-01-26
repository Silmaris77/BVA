-- Rename 'foundation' track to 'associate' in modules table
UPDATE modules
SET track = 'associate'
WHERE track = 'foundation';

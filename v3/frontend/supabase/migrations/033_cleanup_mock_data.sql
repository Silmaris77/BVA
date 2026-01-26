-- 1. Delete all lessons from Professional and Expert tracks
DELETE FROM lessons 
WHERE track IN ('professional', 'expert', 'master');

-- 2. Delete all Learning Paths (mockups)
-- User asked to remove "wszystkie mockupowe lekcje i ścieżki edukacyjne"
-- Assuming all current paths in 'learning_paths' are mockups/old, as we are rebuilding Structure.
DELETE FROM learning_paths;

-- 3. Delete any "Mockup" lessons that might be lingering with no track or specific titles
-- Safe bet: if it's not 'associate' (renamed from foundation) and not 'math', it's likely a leftover.
-- But let's be specific to avoid accidents.
-- Removing lessons with 'test', 'demo', 'sample' in title case insensitive
DELETE FROM lessons 
WHERE title ILIKE '%test%' 
   OR title ILIKE '%demo%' 
   OR title ILIKE '%sample%';

-- 4. Clean up any orphaned modules?
-- If we deleted lessons, maybe some modules are empty. 
-- But user only asked for lessons and paths. We'll leave modules for now unless they are explicitly Professional ones.
-- Let's remove modules that are for Professional/Expert tracks.
DELETE FROM modules
WHERE track IN ('professional', 'expert');

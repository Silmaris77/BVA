-- ============================================
-- CLEANUP & FRESH DEPLOYMENT
-- ============================================
-- Run this in Supabase SQL Editor to clean old data and deploy fresh engrams

-- Step 1: Remove OLD engrams (safe - keeps user progress)
DELETE FROM engrams WHERE engram_id IN (
  'quick_learner1', 
  'quick_learner',
  'milwaukee_expert',
  'master_technician',
  'quick_reference_pro',
  'sales_accelerator',
  'beta_tester',
  'mentor',
  'top_performer'
);

-- Step 2: Verify cleanup
SELECT engram_id, title FROM engrams;

-- Step 3: Deploy fresh engrams
-- (Copy entire seed_milwaukee_engrams.sql BELOW THIS LINE)

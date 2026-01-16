# Supabase Migrations - Installation Guide

## 📋 Migration Files Created

4 migration files w kolejności wykonania:

1. **001_create_content_tables.sql** - Content (lessons, engrams, tools, resources, drills)
2. **002_create_multi_tenancy.sql** - Multi-tenancy (companies, roles, access control)
3. **003_create_learning_paths.sql** - Learning paths + user path progress
4. **004_create_user_progress.sql** - User progress tracking + XP system

---

## 🚀 How to Run Migrations

### Option A: Supabase CLI (Recommended)

```bash
# 1. Navigate to project root
cd c:\Users\pksia\Dropbox\BVA\v3

# 2. Initialize Supabase (if not done)
supabase init

# 3. Link to your Supabase project
supabase link --project-ref YOUR_PROJECT_REF

# 4. Run all migrations
supabase db push

# 5. Verify migrations ran successfully
supabase db diff
```

### Option B: Supabase Dashboard (Manual)

1. Otwórz **Supabase Dashboard** → https://app.supabase.com
2. Wybierz projekt BVA V3
3. Przejdź do **SQL Editor**
4. Dla każdego pliku migration (w kolejności 001 → 004):
   - Skopiuj zawartość SQL
   - Wklej do SQL Editor
   - Kliknij **RUN**
   - Sprawdź czy sukces (zielony checkmark)

### Option C: Supabase Studio (Local Development)

```bash
# 1. Start local Supabase
cd c:\Users\pksia\Dropbox\BVA\v3
supabase start

# 2. Apply migrations
supabase db reset  # Fresh start with all migrations

# 3. Access Studio
# Open http://localhost:54323
```

---

## ✅ Verification Steps

Po uruchomieniu migrations, sprawdź:

### 1. Check Tables Created

```sql
-- Run in SQL Editor
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;
```

**Expected tables (14):**
- companies
- content_access_rules
- drills
- engrams
- learning_paths
- lessons
- resources
- tools
- user_drill_attempts
- user_engram_installs
- user_lesson_progress
- user_path_progress
- user_roles
- user_tool_usage
- user_xp_transactions

### 2. Check Seed Data

```sql
-- Verify 'general' company exists
SELECT * FROM companies WHERE company_slug = 'general';

-- Verify 'learner' role exists
SELECT * FROM user_roles WHERE role_slug = 'learner';
```

**Expected:**
- 1 row in `companies` (General Access)
- 1 row in `user_roles` (Learner)

### 3. Check auth.users Extensions

```sql
-- Check if company_id and role_id columns added
SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_schema = 'auth' 
  AND table_name = 'users'
  AND column_name IN ('company_id', 'role_id', 'department');
```

**Expected:** 3 columns with defaults pointing to 'general' company and 'learner' role

### 4. Test XP Function

```sql
-- Test get_user_total_xp function
SELECT get_user_total_xp('00000000-0000-0000-0000-000000000000'::UUID);
```

**Expected:** 0 (no XP for dummy UUID)

---

## 🔧 Troubleshooting

### Error: "relation already exists"

**Cause:** Migrations already ran or partial run.

**Fix:**
```sql
-- Option 1: Drop and recreate (CAUTION: loses data!)
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

-- Then re-run migrations

-- Option 2: Check which tables exist and run only missing migrations
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
```

### Error: "permission denied for schema auth"

**Cause:** Can't modify `auth.users` table.

**Fix:** Use Supabase Dashboard with service role key:
1. Dashboard → Project Settings → API
2. Copy `service_role` key
3. Use in migration with elevated permissions

### Error: "function update_updated_at_column() does not exist"

**Cause:** Migration 001 didn't complete.

**Fix:** Re-run migration 001 completely.

---

## 📊 Next Steps After Migrations

### 1. Seed Additional Companies

```sql
INSERT INTO companies (company_slug, name) VALUES
  ('milwaukee', 'Milwaukee Tool'),
  ('ryobi', 'Ryobi'),
  ('aeg', 'AEG Power Tools')
ON CONFLICT (company_slug) DO NOTHING;
```

### 2. Seed Additional Roles

```sql
INSERT INTO user_roles (role_slug, display_name, description) VALUES
  ('sales-rep', 'Sales Representative', 'Field sales role'),
  ('manager', 'Manager', 'Team manager role'),
  ('technician', 'Technician', 'Technical support role'),
  ('admin', 'Administrator', 'Platform admin')
ON CONFLICT (role_slug) DO NOTHING;
```

### 3. Create Sample Learning Path

```sql
INSERT INTO learning_paths (
  path_slug,
  title,
  description,
  estimated_hours,
  difficulty,
  total_xp_reward,
  lesson_sequence
) VALUES (
  'automotive-sales-mastery',
  'Automotive Sales Mastery',
  'Kompletna ścieżka dla przedstawicieli handlowych Milwaukee Automotive',
  12,
  'beginner',
  1500,
  '["lesson-1-torque-automotive", "lesson-2-consultative-selling"]'::jsonb
);
```

### 4. Set Up Row Level Security (RLS)

**Important:** Enable RLS on all tables for security!

```sql
-- Enable RLS on all user progress tables
ALTER TABLE user_lesson_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_engram_installs ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_tool_usage ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_drill_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_xp_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_path_progress ENABLE ROW LEVEL SECURITY;

-- Create policies (users can only see their own data)
CREATE POLICY "Users can view own lesson progress"
  ON user_lesson_progress FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own lesson progress"
  ON user_lesson_progress FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own lesson progress"
  ON user_lesson_progress FOR UPDATE
  USING (auth.uid() = user_id);

-- Repeat for other user_ tables...
```

---

## 📝 Migration Summary

**Total Tables Created:** 15 (14 content/progress + auth.users extended)  
**Total Indexes:** 25+  
**Total Functions:** 2 (update_updated_at_column, get_user_total_xp)  
**Seed Data:** 1 company ('general') + 1 role ('learner')

**Database Schema Ready!** ✅

Next: Build API routes to interact with these tables.

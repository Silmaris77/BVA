# Supabase Database Files

This directory contains database schema and seed data for the BrainVenture V3 application.

## Structure

```
supabase/
├── schema.sql              # Main database schema (tables, RLS policies)
└── seeds/                  # Seed data (initial content)
    └── 01_milwaukee_canvas.sql  # Milwaukee Canvas lesson data
```

## How to Use

### 1. Initial Setup (First Time)

Run the schema file in Supabase SQL Editor to create tables:

```sql
-- Copy content from schema.sql and run in Supabase SQL Editor
```

### 2. Seed Data

After schema is created, run seed files in order:

```sql
-- Run seeds/01_milwaukee_canvas.sql to load Milwaukee lesson
```

### 3. Updating Data

To update existing lessons:
- Modify the seed file
- Delete old data: `DELETE FROM lessons WHERE id = 'lesson-id';`
- Re-run the INSERT statement

## Files

### `schema.sql`
- Creates all tables (lessons, engrams, resources, user_progress, etc.)
- Sets up Row Level Security (RLS) policies
- Includes mock data for engrams and resources

### `seeds/01_milwaukee_canvas.sql`
- Milwaukee Application First Canvas lesson
- 26 cards with full content
- Uses PostgreSQL E-string notation for proper newline handling

## Notes

- Always backup data before running SQL scripts in production
- Test scripts in development environment first
- Schema changes may require data migration

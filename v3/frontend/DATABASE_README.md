# Database Files - Quick Reference

## 📁 Location
All database files are now in: **`v3/frontend/supabase/`**

## 🚀 Quick Start

### 1. Initial Database Setup
```bash
# In Supabase Dashboard → SQL Editor
# Copy and run: supabase/schema.sql
```

### 2. Load Lesson Data
```bash
# In Supabase Dashboard → SQL Editor  
# Copy and run: supabase/seeds/01_milwaukee_canvas.sql
```

## 📝 Files

| File | Purpose |
|------|---------|
| `supabase/schema.sql` | Database schema (tables, RLS policies, mock data) |
| `supabase/seeds/01_milwaukee_canvas.sql` | Milwaukee Canvas lesson (26 cards) |
| `supabase/README.md` | Full documentation |

## ⚠️ Important Notes

- **Markdown in lessons works!** All cards now use ReactMarkdown
- Fixed components: `IntroCard`, `PracticeCard`, `QuestionCard`
- Use E-string notation (`E'...'`) in SQL for proper newlines
- Seed files use `jsonb_build_object()` for clean JSON

## 🔗 See Also

- Full docs: [supabase/README.md](./supabase/README.md)
- Lesson JSON source: `data/lessons/milwaukee_canvas_v2.json`

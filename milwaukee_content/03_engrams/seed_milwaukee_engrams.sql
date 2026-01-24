-- ============================================
-- Milwaukee Engrams - Full Catalog Seed
-- ============================================
-- Description: 8 new engrams covering learning boosts, productivity, unlocks, and prestige
-- Based on: milwaukee_content/03_engrams/engrams_list.md
-- Date: 2026-01-22

-- ============================================
-- LEARNING CATEGORY
-- ============================================

-- Engram 1: Quick Learner
INSERT INTO engrams (
  engram_id,
  title,
  category,
  slides,
  quiz_pool,
  install_xp,
  refresh_xp
) VALUES (
  'quick_learner',
  'Quick Learner',
  'learning',
  '[
    {
      "id": "s1",
      "title": "Ucz się szybciej",
      "content": "Quick Learner to Twój pierwszy krok do efektywniejszej nauki. Każde źródło XP będzie teraz dawało 10% więcej."
    },
    {
      "id": "s2", 
      "title": "Jak to działa?",
      "content": "Bonus stosuje się automatycznie do każdej ukończonej lekcji, quizu, engramu czy ćwiczenia. 100 XP → 110 XP."
    },
    {
      "id": "s3",
      "title": "Kiedy się opłaca?",
      "content": "Im więcej się uczysz, tym więcej zyskujesz. Po 10 lekcjach zwróci się koszt instalacji."
    }
  ]'::jsonb,
  '[
    {
      "q": "Jaki bonus XP daje Quick Learner?",
      "a": "+10%",
      "wrong": ["+5%", "+20%", "+15%"]
    },
    {
      "q": "Na co wpływa Quick Learner?",
      "a": "Wszystkie źródła XP",
      "wrong": ["Tylko lekcje", "Tylko quizy", "Tylko engramy"]
    },
    {
      "q": "Kiedy bonus się stosuje?",
      "a": "Automatycznie",
      "wrong": ["Musisz go włączyć", "Tylko w weekendy", "Po każdych 5 lekcjach"]
    }
  ]'::jsonb,
  200,
  50
)
ON CONFLICT (engram_id) DO UPDATE SET
  title = EXCLUDED.title,
  category = EXCLUDED.category,
  slides = EXCLUDED.slides,
  quiz_pool = EXCLUDED.quiz_pool;

-- Engram 2: Milwaukee Expert
INSERT INTO engrams (
  engram_id,
  title,
  category,
  slides,
  quiz_pool,
  install_xp,
  refresh_xp
) VALUES (
  'milwaukee_expert',
  'Milwaukee Expert',
  'learning',
  '[
    {
      "id": "s1",
      "title": "Specjalista od produktów",
      "content": "Milwaukee Expert to zaawansowana wiedza o całej linii produktowej. Odblokowujesz dostęp do specyfikacji technicznych i case studies."
    },
    {
      "id": "s2",
      "title": "Bonusy",
      "content": "• +15% XP na lekcjach product knowledge\n• Dostęp do zaawansowanych specyfikacji\n• Porównania konkurencji\n• Rekomendacje produktowe"
    },
    {
      "id": "s3",
      "title": "Dla kogo?",
      "content": "Dla sprzedawców, ASM-ów i techników, którzy chcą znać produkty Milwaukee jak własną kieszeń."
    }
  ]'::jsonb,
  '[
    {
      "q": "Jaki bonus XP daje Milwaukee Expert na lekcjach produktowych?",
      "a": "+15%",
      "wrong": ["+10%", "+20%", "+25%"]
    },
    {
      "q": "Co odblokowuje Milwaukee Expert?",
      "a": "Zaawansowane specyfikacje",
      "wrong": ["Tylko quizy", "Dostęp premium", "Certyfikaty"]
    },
    {
      "q": "Dla kogo jest Milwaukee Expert?",
      "a": "Sprzedawcy i technicy",
      "wrong": ["Tylko managery", "Wszyscy", "Tylko nowi pracownicy"]
    }
  ]'::jsonb,
  500,
  75
)
ON CONFLICT (engram_id) DO UPDATE SET
  title = EXCLUDED.title,
  category = EXCLUDED.category,
  slides = EXCLUDED.slides,
  quiz_pool = EXCLUDED.quiz_pool;

-- Engram 3: Master Technician
INSERT INTO engrams (
  engram_id,
  title,
  category,
  slides,
  quiz_pool,
  install_xp,
  refresh_xp
) VALUES (
  'master_technician',
  'Master Technician',
  'learning',
  '[
    {
      "id": "s1",
      "title": "Szczyt umiejętności",
      "content": "Master Technician to prestiżowy engram dla najbardziej zaawansowanych użytkowników. Odblokowujesz treści eksperckie i przygotowanie do certyfikacji."
    },
    {
      "id": "s2",
      "title": "Co zyskujesz?",
      "content": "• +20% XP overall\n• Dostęp do lekcji expert-level\n• Przygotowanie do certyfikacji\n• Badge \"Master\" na profilu"
    },
    {
      "id": "s3",
      "title": "Wymagania",
      "content": "Wymagany poziom 10 i 1000 XP. To inwestycja w Twoją długoterminową karierę."
    }
  ]'::jsonb,
  '[
    {
      "q": "Jaki bonus XP daje Master Technician?",
      "a": "+20%",
      "wrong": ["+15%", "+25%", "+30%"]
    },
    {
      "q": "Co odblokowuje Master Technician?",
      "a": "Lekcje eksperckie i certyfikację",
      "wrong": ["Tylko badge", "Tylko XP", "Dostęp do forum"]
    },
    {
      "q": "Jaki poziom jest wymagany?",
      "a": "Poziom 10",
      "wrong": ["Poziom 5", "Poziom 15", "Poziom 20"]
    }
  ]'::jsonb,
  1000,
  100
)
ON CONFLICT (engram_id) DO UPDATE SET
  title = EXCLUDED.title,
  category = EXCLUDED.category,
  slides = EXCLUDED.slides,
  quiz_pool = EXCLUDED.quiz_pool;

-- ============================================
-- PRODUCTIVITY CATEGORY
-- ============================================

-- Engram 4: Quick Reference Pro
INSERT INTO engrams (
  engram_id,
  title,
  category,
  slides,
  quiz_pool,
  install_xp,
  refresh_xp
) VALUES (
  'quick_reference_pro',
  'Quick Reference Pro',
  'productivity',
  '[
    {
      "id": "s1",
      "title": "Informacje pod ręką",
      "content": "Quick Reference Pro daje dostęp offline do wszystkich materiałów i nielimitowane zakładki. Idealne dla pracy w terenie."
    },
    {
      "id": "s2",
      "title": "Funkcje",
      "content": "• Offline access do resources\n• Nielimitowane zakładki\n• Własne cheat sheets\n• Szybkie notatki"
    },
    {
      "id": "s3",
      "title": "Case study",
      "content": "Technik serwisowy przy maszynie bez internetu? Quick Reference ma wszystkie specyfikacje offline."
    }
  ]'::jsonb,
  '[
    {
      "q": "Co daje Quick Reference Pro?",
      "a": "Dostęp offline i zakładki",
      "wrong": ["Tylko XP", "Tylko quizy", "Premium support"]
    },
    {
      "q": "Ile zakładek możesz mieć?",
      "a": "Nielimitowane",
      "wrong": ["10", "50", "100"]
    },
    {
      "q": "Dla kogo jest Quick Reference?",
      "a": "Osoby pracujące w terenie",
      "wrong": ["Tylko biuro", "Tylko managery", "Wszyscy równo"]
    }
  ]'::jsonb,
  300,
  60
)
ON CONFLICT (engram_id) DO UPDATE SET
  title = EXCLUDED.title,
  category = EXCLUDED.category,
  slides = EXCLUDED.slides,
  quiz_pool = EXCLUDED.quiz_pool;

-- Engram 5: Sales Accelerator
INSERT INTO engrams (
  engram_id,
  title,
  category,
  slides,
  quiz_pool,
  install_xp,
  refresh_xp
) VALUES (
  'sales_accelerator',
  'Sales Accelerator',
  'productivity',
  '[
    {
      "id": "s1",
      "title": "Zamykaj deale szybciej",
      "content": "Sales Accelerator odblokowuje zaawansowane narzędzia sprzedażowe: kalkulator ROI, konfigurator, battle cards."
    },
    {
      "id": "s2",
      "title": "Toolkit",
      "content": "• ROI Calculator - pokaż oszczędności\n• Product Configurator - zbuduj zestaw\n• Battle Cards - vs konkurencja\n• Pitch Builder - własne prezentacje"
    },
    {
      "id": "s3",
      "title": "Rezultaty",
      "content": "Sprzedawcy z Sales Accelerator zamykają deale 30% szybciej dzięki gotowym argumentom i kalkulacjom."
    }
  ]'::jsonb,
  '[
    {
      "q": "Co odblokowuje Sales Accelerator?",
      "a": "ROI Calculator i Battle Cards",
      "wrong": ["Tylko quizy", "Dostęp offline", "Badge prestiżowy"]
    },
    {
      "q": "O ile szybciej zamykasz deale?",
      "a": "30%",
      "wrong": ["10%", "50%", "20%"]
    },
    {
      "q": "Co to Battle Cards?",
      "a": "Porównania vs konkurencja",
      "wrong": ["Quiz", "Gra", "Certyfikat"]
    }
  ]'::jsonb,
  600,
  80
)
ON CONFLICT (engram_id) DO UPDATE SET
  title = EXCLUDED.title,
  category = EXCLUDED.category,
  slides = EXCLUDED.slides,
  quiz_pool = EXCLUDED.quiz_pool;

-- ============================================
-- UNLOCKING CATEGORY
-- ============================================

-- Engram 6: Beta Tester
INSERT INTO engrams (
  engram_id,
  title,
  category,
  slides,
  quiz_pool,
  install_xp,
  refresh_xp
) VALUES (
  'beta_tester',
  'Beta Tester',
  'unlocking',
  '[
    {
      "id": "s1",
      "title": "Kształtuj przyszłość Academy",
      "content": "Beta Tester daje early access do nowych lekcji i możliwość wpływania na to, jaki content powstaje."
    },
    {
      "id": "s2",
      "title": "Privileges",
      "content": "• Early access do nowych lekcji\n• Możliwość feedbacku\n• Głosowanie na nowy kontent\n• Badge \"Beta\" na profilu"
    },
    {
      "id": "s3",
      "title": "Odpowiedzialność",
      "content": "Beta Testerzy pomagają wyłapywać błędy i sugerują ulepszenia. Twój feedback ma realny wpływ."
    }
  ]'::jsonb,
  '[
    {
      "q": "Co daje Beta Tester?",
      "a": "Early access i feedback",
      "wrong": ["Tylko XP", "Tylko badge", "Premium support"]
    },
    {
      "q": "Czy możesz głosować na nowy kontent?",
      "a": "Tak",
      "wrong": ["Nie", "Tylko managery", "Po Level 20"]
    },
    {
      "q": "Jaka jest rola Beta Testera?",
      "a": "Wyłapywać błędy i dawać feedback",
      "wrong": ["Tylko uczyć się", "Sprzedawać", "Zarządzać"]
    }
  ]'::jsonb,
  400,
  70
)
ON CONFLICT (engram_id) DO UPDATE SET
  title = EXCLUDED.title,
  category = EXCLUDED.category,
  slides = EXCLUDED.slides,
  quiz_pool = EXCLUDED.quiz_pool;

-- Engram 7: Mentor
INSERT INTO engrams (
  engram_id,
  title,
  category,
  slides,
  quiz_pool,
  install_xp,
  refresh_xp
) VALUES (
  'mentor',
  'Mentor',
  'unlocking',
  '[
    {
      "id": "s1",
      "title": "Dziel się wiedzą",
      "content": "Mentor pozwala tworzyć własne lekcje dla zespołu i śledzić postępy podopiecznych. Dostajesz XP za ich sukcesy."
    },
    {
      "id": "s2",
      "title": "Możliwości",
      "content": "• Twórz custom lessons dla zespołu\n• Śledź postępy mentees\n• +10 XP za każdego, kto kończy moduł\n• Badge \"Mentor\" na profilu"
    },
    {
      "id": "s3",
      "title": "Impact",
      "content": "Dobrzy mentorzy budują silniejsze zespoły. Twoja wiedza przestaje być tylko Twoja - stajesz się force multiplier."
    }
  ]'::jsonb,
  '[
    {
      "q": "Co daje Mentor?",
      "a": "Tworzenie lekcji i tracking zespołu",
      "wrong": ["Tylko XP", "Tylko badge", "Dostęp offline"]
    },
    {
      "q": "Ile XP dostajesz za mentee, który kończy moduł?",
      "a": "+10 XP",
      "wrong": ["+5 XP", "+20 XP", "+50 XP"]
    },
    {
      "q": "Czym jest force multiplier?",
      "a": "Wpływ na wielu ludzi jednocześnie",
      "wrong": ["Bonus XP", "Narzędzie", "Certyfikat"]
    }
  ]'::jsonb,
  800,
  90
)
ON CONFLICT (engram_id) DO UPDATE SET
  title = EXCLUDED.title,
  category = EXCLUDED.category,
  slides = EXCLUDED.slides,
  quiz_pool = EXCLUDED.quiz_pool;

-- ============================================
-- ACHIEVEMENT CATEGORY
-- ============================================

-- Engram 8: Top Performer
INSERT INTO engrams (
  engram_id,
  title,
  category,
  slides,
  quiz_pool,
  install_xp,
  refresh_xp
) VALUES (
  'top_performer',
  'Top Performer',
  'achievement',
  '[
    {
      "id": "s1",
      "title": "Elita Milwaukee Academy",
      "content": "Top Performer to badge prestiżowy dla top 5% użytkowników. Oznacza commitment, skill i consistency."
    },
    {
      "id": "s2",
      "title": "Korzyści",
      "content": "• Złoty badge na profilu\n• Opcjonalne miejsce na leaderboard\n• Dostęp do ekskluzywnej społeczności\n• Network z innymi top performers"
    },
    {
      "id": "s3",
      "title": "Standard",
      "content": "Ten engram kosztuje 1500 XP nie bez powodu. To commitment. Ale efekty są trwałe - raz top performer, zawsze top performer."
    }
  ]'::jsonb,
  '[
    {
      "q": "Jaki % użytkowników ma Top Performer?",
      "a": "Top 5%",
      "wrong": ["Top 10%", "Top 1%", "Top 20%"]
    },
    {
      "q": "Co daje Top Performer?",
      "a": "Badge i dostęp do społeczności",
      "wrong": ["Tylko XP", "Tylko certyfikat", "Darmowe narzędzia"]
    },
    {
      "q": "Czy Top Performer można stracić?",
      "a": "Nie, jest trwały",
      "wrong": ["Tak, po miesiącu", "Tak, jeśli nie logujesz się", "Tak, po roku"]
    }
  ]'::jsonb,
  1500,
  150
)
ON CONFLICT (engram_id) DO UPDATE SET
  title = EXCLUDED.title,
  category = EXCLUDED.category,
  slides = EXCLUDED.slides,
  quiz_pool = EXCLUDED.quiz_pool;

-- ============================================
-- VERIFICATION
-- ============================================

-- Show all engrams by category
SELECT 
  engram_id,
  title,
  category,
  install_xp,
  refresh_xp,
  jsonb_array_length(slides) as slide_count,
  jsonb_array_length(quiz_pool) as quiz_count
FROM engrams
ORDER BY category, install_xp;

-- Success message
DO $$
BEGIN
  RAISE NOTICE '✅ Milwaukee Engrams seeded successfully!';
  RAISE NOTICE '🧠 Total categories: Learning (3), Productivity (2), Unlocking (2), Achievement (1)';
  RAISE NOTICE '📊 XP Range: 200-1500';
END $$;

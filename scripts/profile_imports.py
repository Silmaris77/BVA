"""
Profiling startowania aplikacji - sprawdza co spowalnia
"""

import time
import sys
from pathlib import Path

# Dodaj parent directory do path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def time_import(module_name):
    """Mierzy czas importu modułu"""
    start = time.time()
    __import__(module_name)
    elapsed = time.time() - start
    return elapsed

print("🔍 PROFILING IMPORTÓW APLIKACJI")
print("=" * 60)

modules_to_test = [
    "streamlit",
    "data.users_new",
    "data.repositories.user_repository",
    "data.repositories.business_game_repository",
    "database.models",
    "database.connection",
    "views.business_games",
    "views.admin",
    "views.dashboard",
    "utils.activity_tracker"
]

results = []

for module in modules_to_test:
    try:
        elapsed = time_import(module)
        results.append((module, elapsed))
        print(f"✅ {module:45s} {elapsed:>8.3f}s")
    except ImportError as e:
        print(f"❌ {module:45s} ERROR: {e}")

print("\n" + "=" * 60)
print("📊 PODSUMOWANIE (posortowane od najwolniejszych)")
print("=" * 60)

results.sort(key=lambda x: x[1], reverse=True)
for module, elapsed in results:
    bar = "█" * int(elapsed * 20)
    print(f"{module:45s} {elapsed:>8.3f}s {bar}")

total = sum(r[1] for r in results)
print("\n" + "=" * 60)
print(f"⏱️  CAŁKOWITY CZAS: {total:.3f}s")
print("=" * 60)

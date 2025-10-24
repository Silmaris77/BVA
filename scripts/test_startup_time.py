"""
Test czasu startu aplikacji Streamlit
"""

import time
import subprocess
import sys

print("🚀 TEST CZASU STARTU APLIKACJI")
print("=" * 60)

start_time = time.time()

# Uruchom Streamlit w tle i zmierz czas do ready
# Uwaga: to tylko symulacja - prawdziwy czas to obserwacja użytkownika

print("⏱️  Importuję główne moduły...")

modules = [
    ("streamlit", "import streamlit as st"),
    ("main.py", "import main"),
]

for name, code in modules:
    module_start = time.time()
    try:
        exec(code)
        elapsed = time.time() - module_start
        print(f"  ✅ {name:20s} {elapsed:>8.3f}s")
    except Exception as e:
        print(f"  ❌ {name:20s} ERROR: {e}")

total = time.time() - start_time
print("\n" + "=" * 60)
print(f"⏱️  CAŁKOWITY CZAS STARTU: {total:.3f}s")
print("=" * 60)

print("\n💡 REKOMENDACJE:")
if total > 5.0:
    print("❌ Aplikacja startuje WOLNO (>5s)")
    print("   Zalecenia:")
    print("   1. Sprawdź czy dual-write jest wyłączony dla odczytu")
    print("   2. Użyj lazy imports w ciężkich modułach")
    print("   3. Rozważ async loading dla Business Games")
elif total > 3.0:
    print("⚠️  Aplikacja startuje średnio (3-5s)")
    print("   Można poprawić lazy loading")
else:
    print("✅ Aplikacja startuje SZYBKO (<3s)")

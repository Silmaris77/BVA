"""
Test bezpośredniego wywołania funkcji evaluate_with_ai()
Pokaże dokładny błąd, jeśli wystąpi
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("="*60)
print("   TEST OCENY AI (GEMINI)")
print("="*60)
print()

# Mock contract
mock_contract = {
    "id": "test_001",
    "tytul": "Test kontraktu",
    "kategoria": "Coaching",
    "poziom_trudnosci": 3,
    "opis": "Zespół ma problemy z komunikacją.",
    "min_slow": 30
}

mock_solution = """
Zespół powinien wprowadzić daily stand-upy, aby poprawić komunikację.
Regularne spotkania pomogą członkom zespołu synchronizować się 
i rozwiązywać problemy na bieżąco.
"""

print("📝 Test contract:")
print(f"   Tytuł: {mock_contract['tytul']}")
print(f"   Kategoria: {mock_contract['kategoria']}")
print(f"   Trudność: {mock_contract['poziom_trudnosci']}")
print()

print("📄 Test solution:")
print(f"   Długość: {len(mock_solution.split())} słów")
print()

print("-"*60)
print("🔄 Wywołuję funkcję evaluate_with_ai()...")
print("-"*60)
print()

try:
    from utils.business_game_evaluation import evaluate_with_ai
    
    rating, feedback, details = evaluate_with_ai(mock_solution, mock_contract)
    
    print("✅ SUKCES! Funkcja zwróciła wynik:")
    print()
    print(f"⭐ Rating: {rating}/5")
    print()
    print("💬 Feedback:")
    print(feedback)
    print()
    print("📊 Szczegóły:")
    import json
    print(json.dumps(details, indent=2, ensure_ascii=False))
    
except Exception as e:
    print(f"❌ BŁĄD: {e}")
    print()
    import traceback
    print("📋 Stack trace:")
    traceback.print_exc()
    print()
    print("="*60)
    print("🔍 DIAGNOZA:")
    print("="*60)
    
    # Sprawdź API key
    print("\n1️⃣ API Key:")
    try:
        import streamlit as st
        key = st.secrets.get("GOOGLE_API_KEY")
        if key:
            print(f"   ✅ st.secrets: {key[:10]}...{key[-5:]}")
        else:
            print("   ❌ Brak w st.secrets")
    except Exception as e2:
        print(f"   ⚠️ Błąd odczytu secrets: {e2}")
    
    # Sprawdź import
    print("\n2️⃣ Import google.generativeai:")
    try:
        import google.generativeai as genai
        print(f"   ✅ Import OK, wersja: {genai.__version__}")
    except ImportError as e3:
        print(f"   ❌ Błąd importu: {e3}")
    
    print()
    print("="*60)
    print("💡 SUGESTIE:")
    print("="*60)
    print("1. Sprawdź czy API key jest poprawny")
    print("2. Sprawdź czy masz dostęp do internetu")
    print("3. Sprawdź limity API Google Gemini")
    print("4. Sprawdź czy kontrakt ma pole 'poziom_trudnosci'")

print()
print("="*60)

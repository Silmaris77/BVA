"""
Naprawia uszkodzony plik JSON users_data.json
"""
import json
import shutil
from datetime import datetime

# Backup
backup_file = f"users_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
shutil.copy('users_data.json', backup_file)
print(f"✅ Backup utworzony: {backup_file}")

# Próba lokalizacji błędu
try:
    with open('users_data.json', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pozycja błędu: znak 542942
    error_pos = 542942
    
    # Pokaż fragment wokół błędu
    print(f"\n📍 Fragment wokół pozycji {error_pos}:")
    print("=" * 80)
    start = max(0, error_pos - 200)
    end = min(len(content), error_pos + 200)
    fragment = content[start:end]
    
    # Zaznacz pozycję błędu
    relative_pos = error_pos - start
    print(fragment[:relative_pos])
    print(">>> TUTAJ BŁĄD <<<")
    print(fragment[relative_pos:])
    print("=" * 80)
    
    # Spróbuj znaleźć linię
    lines_before = content[:error_pos].count('\n')
    print(f"\n📊 Linia {lines_before + 1}")
    
    # Próba naprawy - znajdź najbliższy poprawny punkt
    print("\n🔧 Próba naprawy...")
    
    # Strategia: usuń nieprawidłowy znak lub dodaj brakujący przecinek
    # Sprawdźmy co jest na pozycji błędu
    char_at_error = content[error_pos] if error_pos < len(content) else 'EOF'
    print(f"Znak na pozycji błędu: '{char_at_error}'")
    
    # Spróbuj załadować JSON i pokaż szczegóły błędu
    json.loads(content)
    
except json.JSONDecodeError as e:
    print(f"\n❌ Błąd JSON: {e}")
    print(f"   Pozycja: {e.pos}")
    print(f"   Linia: {e.lineno}, Kolumna: {e.colno}")
    
    # Pokaż fragment wokół błędu z pozycji JSONDecodeError
    if e.pos:
        start = max(0, e.pos - 300)
        end = min(len(content), e.pos + 300)
        fragment = content[start:end]
        relative_pos = e.pos - start
        
        print(f"\n📍 Fragment JSON wokół błędu:")
        print("=" * 80)
        print(fragment[:relative_pos])
        print("\n>>> BŁĄD TUTAJ <<<\n")
        print(fragment[relative_pos:relative_pos+100])
        print("=" * 80)
        
        # Analiza struktury
        print("\n🔍 Analiza:")
        before = content[max(0, e.pos-50):e.pos]
        after = content[e.pos:min(len(content), e.pos+50)]
        print(f"Przed błędem (50 znaków): ...{before}")
        print(f"Po błędzie (50 znaków): {after}...")
        
        # Sugestie naprawy
        print("\n💡 Możliwe rozwiązania:")
        if "Expecting ',' delimiter" in str(e):
            print("   1. Brakuje przecinka między elementami")
            print("   2. Nieprawidłowy znak w miejscu przecinka")
            print("   3. Dodatkowy cudzysłów lub nawias")

print("\n✅ Analiza zakończona. Sprawdź wyniki powyżej.")

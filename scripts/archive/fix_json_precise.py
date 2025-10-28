"""
Naprawia błąd JSON - dokładna lokalizacja
"""
import json
import shutil
from datetime import datetime

# Backup
backup_file = f"users_data_backup_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
shutil.copy('users_data.json', backup_file)
print(f"✅ Backup: {backup_file}")

# Wczytaj
with open('users_data.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Błąd na pozycji 542942
error_pos = 542942

print(f"📍 Pozycja błędu: {error_pos}")
print(f"Znak na tej pozycji: {repr(content[error_pos])}")
print(f"\n🔍 Fragment 100 znaków przed błędem:")
print(repr(content[error_pos-100:error_pos]))
print(f"\n🔍 Fragment 100 znaków po błędzie:")
print(repr(content[error_pos:error_pos+100]))

# Znajdź początek problematycznego stringa
# Szukamy wstecz ostatniego "
quote_before = content.rfind('"', 0, error_pos)
quote_after = content.find('"', error_pos)

print(f"\n📝 String od pozycji {quote_before} do {quote_after}:")
problematic_string = content[quote_before:quote_after+1]
print(repr(problematic_string[:200]))

# Sprawdź czy w stringu są nieprawidłowe znaki nowej linii
if '\n' in problematic_string[1:-1]:  # Pomijamy cudzysłowy na początku i końcu
    print("\n⚠️ ZNALEZIONO: Dosłowne znaki nowej linii wewnątrz JSON stringa!")
    print("To jest problem - w JSON stringach powinno być \\n (escaped), nie dosłowne nowe linie")
    
    # Napraw wszystkie takie przypadki w całym pliku
    print("\n🔧 Naprawiam wszystkie JSON stringi...")
    
    # Strategia: znajdź wszystkie stringi z dosłownymi \n i zamień je na escaped \\n
    # Ale to trudne... Prostsze: użyj json.loads z odzyskiwaniem
    
    # Albo prostsze rozwiązanie: w kontekście JSON stringów zamień \n na spację
    # Musimy to zrobić ostrożnie, żeby nie zepsuć prawidłowych escaped \\n
    
    # Znajdźmy wszystkie miejsca gdzie jest dosłowny \n między cudzysłowami
    import re
    
    # Wzorzec: " ... \n ... " (gdzie \n to dosłowny znak, nie \\n)
    # To jest trudne w regex...
    
    # Prostsze podejście: zamień w problematycznym fragmencie
    # Fragment z błędu to obszar od ostatniego { do najbliższego }
    
    obj_start = content.rfind('{', 0, error_pos)
    obj_end = content.find('}', error_pos)
    
    print(f"\n🎯 Problematyczny obiekt: pozycje {obj_start} - {obj_end}")
    
    # Weź wartość klucza która ma problem
    # Szukamy key: "value with \n inside"
    
    # Fragment przed błędem pokazuje: ...Klient\npodnosi...
    # Znajdźmy cały ten string
    
    # Szukaj wstecz do początku stringa
    string_start = content.rfind('"', obj_start, error_pos - 1)  # -1 bo error_pos to już 'p'
    string_end = content.find('"', error_pos)
    
    bad_string = content[string_start:string_end+1]
    print(f"\n❌ Zły string (pierwsze 300 znaków):")
    print(repr(bad_string[:300]))
    
    # Napraw ten string - zamień dosłowne \n na \\n (escaped)
    fixed_string = bad_string.replace('\n', '\\n')
    
    print(f"\n✅ Naprawiony string (pierwsze 300 znaków):")
    print(repr(fixed_string[:300]))
    
    # Zastosuj naprawę
    content_fixed = content[:string_start] + fixed_string + content[string_end+1:]
    
    # Sprawdź
    try:
        data = json.loads(content_fixed)
        print("\n✅✅✅ JSON POPRAWNY!")
        
        # Zapisz
        with open('users_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("✅ Plik naprawiony i zapisany!")
        
    except json.JSONDecodeError as e:
        print(f"\n❌ Wciąż błąd: {e}")
        # Zapisz naprawioną wersję do testowania
        with open('users_data_attempted_fix.json', 'w', encoding='utf-8') as f:
            f.write(content_fixed)
        print("⚠️ Zapisano próbę naprawy do users_data_attempted_fix.json")

else:
    print("\n🤔 Brak dosłownych \\n w tym stringu...")
    print("Inny problem - sprawdzam dalej...")

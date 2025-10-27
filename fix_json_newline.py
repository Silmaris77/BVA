"""
Naprawia błąd z nieprawidłowym znakiem nowej linii w users_data.json
"""
import json
import shutil
from datetime import datetime

# Backup (jeśli jeszcze nie ma)
backup_file = f"users_data_backup_emergency_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
shutil.copy('users_data.json', backup_file)
print(f"✅ Emergency backup: {backup_file}")

# Wczytaj plik jako tekst
with open('users_data.json', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"📊 Długość pliku: {len(content)} znaków")

# Pozycja błędu: 542942
# Problem: "Klient\npodnosi budżet" - powinno być "Klient podnosi budżet"
# Szukamy tego fragmentu

# Znajdź problematyczny fragment
search_text = '"Klient'
pos = content.find(search_text, 542900)

if pos != -1:
    print(f"\n📍 Znaleziono na pozycji {pos}")
    fragment = content[pos:pos+100]
    print(f"Fragment: {repr(fragment)}")
    
    # Sprawdź czy to ten problem
    if '\npodnosi' in fragment or '\\npodnosi' in fragment:
        print("✅ Potwierdzono problem: nieprawidłowa nowa linia")
        
        # Naprawa 1: Zamień wszystkie literalne \n w stringach na spacje (ale nie w escape sequences)
        # W JSON stringach powinny być \\n (escaped), a nie dosłowne nowe linie
        
        # Spróbujmy innego podejścia - znajdź cały JSON object i napraw go
        # Szukamy fragmentu z problemem
        start = content.rfind('{', 0, 542942)  # Początek obiektu
        end = content.find('}', 542942) + 1     # Koniec obiektu
        
        print(f"\nObiekt od {start} do {end}")
        problematic_object = content[start:end]
        
        # Pokaż fragment
        print("\n🔍 Problematyczny obiekt (pierwsze 500 znaków):")
        print(problematic_object[:500])
        
        # Naprawa: w stringach JSON zamień dosłowne nowe linie na spacje
        # Ale tylko w kontekście stringa, nie w całym pliku
        
        # Prostsze rozwiązanie: znajdź i zamień konkretny problematyczny fragment
        old_fragment = '"Klient\npodnosi budżet'
        new_fragment = '"Klient podnosi budżet'
        
        if old_fragment in content:
            print(f"\n🔧 Zamieniam: {repr(old_fragment)}")
            print(f"         na: {repr(new_fragment)}")
            content_fixed = content.replace(old_fragment, new_fragment)
            
            # Sprawdź czy naprawione
            try:
                data = json.loads(content_fixed)
                print("✅ JSON poprawny po naprawie!")
                
                # Zapisz naprawiony plik
                with open('users_data.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print("✅ Plik zapisany i sformatowany")
                print(f"📊 Liczba użytkowników: {len(data)}")
                
            except json.JSONDecodeError as e:
                print(f"❌ Wciąż błąd JSON: {e}")
                print("   Potrzebna głębsza analiza...")
        else:
            # Może jest w innej formie?
            print("\n🔍 Szukam innych wariantów...")
            # Sprawdź czy może być jako escaped
            variants = [
                'Klient\\npodnosi budżet',
                'Klient\npodnosi',
                '"Klient" + "\npodnosi',
            ]
            for v in variants:
                if v in content:
                    print(f"   Znaleziono wariant: {repr(v)}")
    else:
        print("⚠️ To nie ten fragment - kontynuuj szukanie...")
        # Pokaż więcej kontekstu
        print(f"Szersszy fragment: {content[pos:pos+200]}")
else:
    print("❌ Nie znaleziono fragmentu 'Klient' w okolicy błędu")
    print("\n🔍 Pokazuję dokładną pozycję błędu:")
    print(repr(content[542930:542960]))

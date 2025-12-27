"""
Skrypt migracji lekcji Conversational Intelligence z formatu v1.0 do v2.0
Przenosi treści ze starego pliku do nowego szkieletu
"""

import json
import os

# Ścieżki plików
OLD_FILE = r"c:\Users\pksia\Dropbox\BVA\data\lessons\11_Conversational_Intelligence_V2_FULL.json"
SKELETON_FILE = r"c:\Users\pksia\Dropbox\BVA\data\lessons\11_Conversational_Intelligence_V2_SKELETON.json"
BACKUP_FILE = r"c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence_BACKUP.json"

# Backup obecnego pliku
current_file = r"c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence.json"
if os.path.exists(current_file):
    with open(current_file, 'r', encoding='utf-8') as f:
        with open(BACKUP_FILE, 'w', encoding='utf-8') as backup:
            backup.write(f.read())
    print(f"✅ Backup utworzony: {BACKUP_FILE}")

# Wczytaj stary plik
print(f"📖 Wczytywanie starego pliku: {OLD_FILE}")
with open(OLD_FILE, 'r', encoding='utf-8') as f:
    old_data = json.load(f)

# Wczytaj nowy szkielet
print(f"📖 Wczytywanie szkieletu: {SKELETON_FILE}")
with open(SKELETON_FILE, 'r', encoding='utf-8') as f:
    new_data = json.load(f)

# Aktualizuj template info
new_data["_template_info"]["status"] = "complete - migrated from v1.0"
new_data["_template_info"]["last_updated"] = "2025-12-24"

# Migruj wprowadzenie
if "intro" in old_data:
    if "main" in old_data["intro"]:
        new_data["wprowadzenie"]["glowny"] = old_data["intro"]["main"]
        print("✅ Zmigrowano: wprowadzenie -> glowny")
    
    if "case_study" in old_data["intro"]:
        new_data["wprowadzenie"]["case_study"] = {
            "title": "Opening Case Study - Rozmowa, która poszła nie tak",
            "description": "Historia Marty i zespołu marketingowego",
            "content": old_data["intro"]["case_study"],
            "questions": [
                "Co, Twoim zdaniem, wydarzyło się w tej rozmowie na poziomie emocji i zaufania?",
                "Jakie reakcje chemiczne mogły zajść w mózgach uczestników tej rozmowy?"
            ]
        }
        print("✅ Zmigrowano: wprowadzenie -> case_study")
    
    if "quiz_samodiagnozy" in old_data["intro"]:
        new_data["wprowadzenie"]["quiz_samodiagnozy"] = old_data["intro"]["quiz_samodiagnozy"]
        print("✅ Zmigrowano: wprowadzenie -> quiz_samodiagnozy")

# Migruj sekcję nauki
if "sections" in old_data and "learning" in old_data["sections"]:
    learning = old_data["sections"]["learning"]
    
    if "tabs" in learning:
        for tab in learning["tabs"]:
            tab_id = tab.get("id", "")
            
            # Tekst
            if tab_id == "tekst" and "sections" in tab:
                new_data["nauka"]["tabs"]["tekst"]["sekcje"] = tab["sections"]
                print(f"✅ Zmigrowano: nauka -> tekst ({len(tab['sections'])} sekcji)")
            
            # Podcast
            elif tab_id == "podcast" and "sections" in tab:
                new_data["nauka"]["tabs"]["podcast"]["sections"] = tab["sections"]
                print(f"✅ Zmigrowano: nauka -> podcast")
            
            # Video
            elif tab_id == "video" and "sections" in tab:
                new_data["nauka"]["tabs"]["video"]["sections"] = tab["sections"]
                print(f"✅ Zmigrowano: nauka -> video")

# Migruj praktykę
if "practical_exercises" in old_data:
    # Główna treść praktyki (jeśli istnieje)
    new_data["praktyka"]["glowny"] = "<div style='padding: 20px;'><p>Ćwiczenia praktyczne C-IQ w działaniu</p></div>"
    
    # Ćwiczenia (case studies)
    if "case_studies" in old_data["practical_exercises"]:
        new_data["praktyka"]["cwiczenia"] = old_data["practical_exercises"]["case_studies"]
        print(f"✅ Zmigrowano: praktyka -> ćwiczenia ({len(old_data['practical_exercises']['case_studies'])} case studies)")

# Migruj podsumowanie
if "sections" in old_data and "summary" in old_data["sections"]:
    summary = old_data["sections"]["summary"]
    
    if "main" in summary:
        new_data["podsumowanie"]["glowny"] = summary["main"]
        print("✅ Zmigrowano: podsumowanie -> glowny")
    
    if "case_study" in summary:
        new_data["podsumowanie"]["case_study"] = summary["case_study"]
        print("✅ Zmigrowano: podsumowanie -> case_study")
    
    if "mind_map" in summary:
        new_data["podsumowanie"]["mapa_mysli"] = summary["mind_map"]
        print("✅ Zmigrowano: podsumowanie -> mapa_mysli")

# Zapisz nowy plik
output_file = r"c:\Users\pksia\Dropbox\BVA\data\lessons\11. Od słów do zaufania - Conversational Intelligence.json"
print(f"\n💾 Zapisywanie zmigrowanego pliku: {output_file}")
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print("\n" + "="*60)
print("✅ MIGRACJA ZAKOŃCZONA POMYŚLNIE!")
print("="*60)
print(f"\n📁 Nowy plik: {output_file}")
print(f"📁 Backup: {BACKUP_FILE}")
print("\n🎯 Następne kroki:")
print("1. Sprawdź plik w aplikacji Streamlit")
print("2. Zweryfikuj poprawność wyświetlania wszystkich sekcji")
print("3. Jeśli wszystko OK, usuń pliki tymczasowe")

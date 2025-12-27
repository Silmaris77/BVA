import json

# Wczytaj istniejący plik (bez ostatniego summary)
with open('data/lessons/MILWAUKEE_Application_First_Canvas.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Usuń niepełną sekcję summary na końcu
if content.endswith(',\n    "summary": {\n'):
    content = content[:-len(',\n    "summary": {\n')]
elif content.endswith(',\r\n    "summary": {\r\n'):
    content = content[:-len(',\r\n    "summary": {\r\n')]

# Dodaj poprawną sekcję summary
summary_content = ''',
    "summary": {
      "main": "<div class='header'><h2 style='text-align: center;'>🎓 Gratulacje! Ukończyłeś Application First Canvas</h2></div><div class='success-box'><h3>✅ Kompletny Checklist Canvas - gotowy do druku</h3><p>Teraz znasz 7-krokową strukturę Application First Canvas. Wydrukuj checklist i zabierz go na pierwsze wizyty!</p></div>"
    }
  }
}'''

# Zapisz naprawiony plik
with open('data/lessons/MILWAUKEE_Application_First_Canvas.json', 'w', encoding='utf-8') as f:
    f.write(content + summary_content)

# Weryfikuj
with open('data/lessons/MILWAUKEE_Application_First_Canvas.json', 'r', encoding='utf-8') as f:
    canvas = json.load(f)
    
print("✅ JSON naprawiony!")
print(f"Ma intro: {'intro' in canvas}")
print(f"Ma sections: {'sections' in canvas}")
print(f"Ma exercises: {'exercises' in canvas}")
print(f"Ma summary: {'summary' in canvas}")
print(f"Tytuł: {canvas.get('title')}")

import codecs

# Read the file
with codecs.open('views/tools.py', 'r', 'utf-8') as f:
    content = f.read()

# Communication Analyzer emoji fixes
replacements = {
    # Tab names (lines 3395-3397)
    '"?? Upload Danych"': '"📤 Upload Danych"',
    '"?? Profil Przywódczy"': '"👤 Profil Przywódczy"',
    '"?? Plan Rozwoju"': '"📋 Plan Rozwoju"',
    
    # Success/info messages
    '?? Wczytano Twój zapisany profil przywódczy': '✅ Wczytano Twój zapisany profil przywódczy',
    
    # Section headers
    '**?? Twój raport będzie zawierał:**': '**📊 Twój raport będzie zawierał:**',
    
    # Spinner messages
    '"?? Tworzę Twój profil przywódczy..."': '"🔄 Tworzę Twój profil przywódczy..."',
    
    # Success messages for profile
    '"? Profil': '"✅ Profil',
    
    # Buttons
    '"?? Użyj przykładów"': '"💡 Użyj przykładów"',
    '"?? Wyczyść pola"': '"🗑️ Wyczyść pola"',
    
    # PDF export (line 5736)
    '"?? Plan Rozwoju Przywódczego"': '"📋 Plan Rozwoju Przywódczego"',
}

# Apply replacements
for old, new in replacements.items():
    content = content.replace(old, new)

# Save the file
with codecs.open('views/tools.py', 'w', 'utf-8') as f:
    f.write(content)

print("✅ Fixed communication analyzer emoji placeholders!")
print("\nFixed items:")
for old, new in replacements.items():
    print(f"  {old} → {new}")

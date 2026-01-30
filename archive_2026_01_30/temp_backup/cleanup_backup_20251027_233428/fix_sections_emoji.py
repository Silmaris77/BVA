import codecs

# Read the file
with codecs.open('views/tools.py', 'r', 'utf-8') as f:
    content = f.read()

# Section headers and field labels emoji fixes
replacements = {
    # Report sections (lines 3409-3421)
    '**?? Poziomy C-IQ**': '**📊 Poziomy C-IQ**',
    '**?? Neurobiologia**': '**🧠 Neurobiologia**',
    '**?? Skuteczność**': '**✅ Skuteczność**',
    
    # Field labels (lines 3493-3518)
    '**?? Rozmowy z zespołem:**': '**💬 Rozmowy z zespołem:**',
    '**?? Motywowanie zespołu:**': '**🎯 Motywowanie zespołu:**',
}

# Apply replacements
count = 0
for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        count += 1
        print(f"✅ {old} → {new}")

# Save the file
with codecs.open('views/tools.py', 'w', 'utf-8') as f:
    f.write(content)

print(f"\n✅ Naprawiono {count} emoji placeholders!")

import re

file_path = r'c:\Users\pksia\Dropbox\BVA\data\lessons\MILWAUKEE_Application_First_Canvas.json'

# Read file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Cyrillic characters
# Find "odkręcaивание" and replace with "odkręcanie"
content = content.replace('odkręcaивание', 'odkręcanie')

# Remove any remaining Cyrillic
content = re.sub(r'[а-яА-ЯёЁ]+', '', content)

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Usunięto cyrylicę z pliku")

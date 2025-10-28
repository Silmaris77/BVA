"""Quick fix for BusinessGameRepository - replace model names with self.Model"""

import re

file_path = "data/repositories/business_game_repository.py"

# Read file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace patterns
replacements = [
    (r'session\.query\(User\)', 'session.query(self.User)'),
    (r'session\.query\(BusinessGame\)', 'session.query(self.BusinessGame)'),
    (r'session\.query\(BusinessGameEmployee\)', 'session.query(self.BusinessGameEmployee)'),
    (r'session\.query\(BusinessGameContract\)', 'session.query(self.BusinessGameContract)'),
    (r'session\.query\(BusinessGameTransaction\)', 'session.query(self.BusinessGameTransaction)'),
    (r'session\.query\(BusinessGameStats\)', 'session.query(self.BusinessGameStats)'),
    (r'BusinessGame\.from_dict', 'self.BusinessGame.from_dict'),
    (r'BusinessGameEmployee\.from_dict', 'self.BusinessGameEmployee.from_dict'),
    (r'BusinessGameContract\.from_dict', 'self.BusinessGameContract.from_dict'),
    (r'BusinessGameTransaction\.from_dict', 'self.BusinessGameTransaction.from_dict'),
    (r'BusinessGameStats\.from_dict', 'self.BusinessGameStats.from_dict'),
]

original = content
for pattern, replacement in replacements:
    content = re.sub(pattern, replacement, content)

if content != original:
    # Backup
    with open(file_path + '.bak', 'w', encoding='utf-8') as f:
        f.write(original)
    
    # Save fixed
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed BusinessGameRepository!")
    print(f"📂 Backup: {file_path}.bak")
else:
    print("⚠️  No changes needed")

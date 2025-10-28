"""Fix save_user_data -> save_single_user in contract_card.py"""

file_path = "views/business_games_refactored/components/contract_card.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all occurrences
content = content.replace('save_user_data(username, user_data)', 'save_single_user(username, user_data)')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed all save_user_data -> save_single_user")

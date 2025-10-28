import json
import shutil
from pathlib import Path

# Backup przed usunięciem
print("Creating backup...")
shutil.copy('users_data.json', 'users_data_backup_before_mick_delete.json')
print("✓ Backup created: users_data_backup_before_mick_delete.json")

# Wczytaj dane
print("\nLoading users_data.json...")
with open('users_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total users before: {len(data)}")

# Usuń użytkownika mick
if 'mick' in data:
    removed = data.pop('mick')
    print("\n✓ User 'mick' removed successfully")
    print(f"  - User ID: {removed.get('user_id', 'N/A')}")
    print(f"  - Had business games: {'business_games' in removed}")
else:
    print("\n⚠ User 'mick' not found in data")

print(f"\nTotal users after: {len(data)}")

# Zapisz
print("\nSaving updated users_data.json...")
with open('users_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✓ File saved successfully")
print("\nDone! 🎉")

import json
import sys

try:
    with open('data/lessons/MILWAUKEE_Application_First_Canvas.json', encoding='utf-8') as f:
        data = json.load(f)
    
    print('✅ JSON valid!')
    print(f'Lesson ID: {data["id"]}')
    print(f'Has summary.main: {"main" in data.get("summary", {})}')
    summary_content = data.get("summary", {}).get("main", "")
    print(f'Summary length: {len(summary_content)} chars')
    print(f'Has action_today: {"action_today" in summary_content}')
    print(f'Has reflection_discovery: {"reflection_discovery" in summary_content}')
    
except json.JSONDecodeError as e:
    print(f'❌ JSON Error: {e}')
    sys.exit(1)
except Exception as e:
    print(f'❌ Error: {e}')
    sys.exit(1)

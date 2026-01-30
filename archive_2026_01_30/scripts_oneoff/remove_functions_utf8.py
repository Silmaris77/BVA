#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Usuwa tylko wyodrębnione funkcje z business_games.py, zachowując UTF-8"""

# Wczytaj plik z UTF-8
with open('views/business_games.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Oryginalny plik: {len(lines)} linii")

# Lista funkcji do usunięcia wraz z zakresami linii (1-based)
# Format: (nazwa, start_line, end_line_exclusive)
functions_to_remove = [
    # helpers.py (82-133, przed innymi funkcjami)
    ('get_contract_reward_coins', 82, 90),
    ('get_contract_reward_reputation', 90, 98),
    ('get_game_data', 98, 109),
    ('save_game_data', 109, 120),
    ('play_coin_sound', 120, 134),  # Zakładam że kończy się około 134
]

# Najpierw usuń helpers (od końca do przodu, żeby nie psuć indeksów)
for func_name, start, end in reversed(functions_to_remove):
    start_idx = start - 1  # 0-based
    end_idx = end - 1
    removed = end_idx - start_idx + 1
    del lines[start_idx:end_idx + 1]
    print(f"  Usunięto {func_name}: linie {start}-{end} ({removed} linii)")

# Zapisz plik tymczasowo, żeby znaleźć nowe pozycje pozostałych funkcji
temp_content = ''.join(lines)
with open('views/business_games_temp.py', 'w', encoding='utf-8') as f:
    f.write(temp_content)

# Teraz znajdź pozostałe funkcje w tymczasowym pliku
print("\nSzukam pozostałych funkcji...")
import re

# Znajdź funkcje do usunięcia (charts, headers, event_card, contract_card)
other_functions = [
    'create_financial_chart',
    'render_header',
    'render_fmcg_header',
    'render_active_effects_badge',
    'render_latest_event_card',
    'show_active_event_card',
    'render_active_contract_card',
    'render_decision_tree_contract',
    'render_conversation_contract',
    'render_speed_challenge_contract',
    'render_contract_card',
    'render_completed_contract_card',
]

# Wczytaj temp file
with open('views/business_games_temp.py', 'r', encoding='utf-8') as f:
    temp_lines = f.readlines()

# Dla każdej funkcji znajdź zakres
ranges = []
for func_name in other_functions:
    pattern = rf'^def {func_name}\('
    for i, line in enumerate(temp_lines):
        if re.match(pattern, line):
            # Znajdź koniec funkcji (następna def na tym samym poziomie wcięcia)
            indent = len(line) - len(line.lstrip())
            end_idx = None
            for j in range(i + 1, len(temp_lines)):
                next_line = temp_lines[j]
                if next_line.strip() and not next_line.startswith('#'):
                    next_indent = len(next_line) - len(next_line.lstrip())
                    if next_indent <= indent and (next_line.strip().startswith('def ') or next_line.strip().startswith('class ') or next_line.strip().startswith('@')):
                        end_idx = j
                        break
            
            if end_idx is None:
                end_idx = len(temp_lines)
            
            ranges.append((func_name, i, end_idx))
            break

# Usuń od końca
ranges.sort(key=lambda x: x[1], reverse=True)
for func_name, start_idx, end_idx in ranges:
    removed = end_idx - start_idx
    del temp_lines[start_idx:end_idx]
    print(f"  Usunięto {func_name}: linie {start_idx+1}-{end_idx} ({removed} linii)")

# Zapisz ostateczny plik
with open('views/business_games.py', 'w', encoding='utf-8') as f:
    f.writelines(temp_lines)

# Usuń temp
import os
os.remove('views/business_games_temp.py')

print(f"\n✅ Nowy plik: {len(temp_lines)} linii")
print(f"✅ Encoding: UTF-8 zachowany")

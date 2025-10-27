#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Usuwa stare funkcje z business_games.py zachowując encoding UTF-8"""

# Funkcje do usunięcia (tylko te, które zostały wyodrębnione do modułów)
FUNCTIONS_TO_REMOVE = [
    ('render_completed_contract_card', 6751, 7059),  # contract_card.py
    ('render_contract_card', 4810, 6750),  # contract_card.py
    ('render_speed_challenge_contract', 4434, 4809),  # contract_card.py
    ('render_conversation_contract', 3804, 4433),  # contract_card.py
    ('render_decision_tree_contract', 3388, 3803),  # contract_card.py
    ('render_active_contract_card', 2989, 3387),  # contract_card.py
    ('show_active_event_card', 2872, 2988),  # event_card.py
    ('render_latest_event_card', 2768, 2871),  # event_card.py
    ('render_active_effects_badge', 2690, 2767),  # event_card.py
    ('render_fmcg_header', 2591, 2689),  # headers.py
    ('render_header', 2483, 2590),  # headers.py
    ('create_financial_chart', 2253, 2482),  # charts.py
    ('play_coin_sound', 2238, 2252),  # helpers.py (było calculate_replay_value - BŁĄD!)
    ('save_game_data', 2218, 2237),  # helpers.py (było trigger_bonus_event - BŁĄD!)
    ('get_game_data', 2187, 2217),  # helpers.py (było get_random_event - BŁĄD!)
    ('get_contract_reward_reputation', 2172, 2186),  # helpers.py (było calculate_reputation_change - BŁĄD!)
    ('get_contract_reward_coins', 2149, 2171),  # helpers.py (było calculate_financial_impact - BŁĄD!)
]

# Wczytaj plik
with open('views/business_games.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Oryginalny plik: {len(lines)} linii")

# Usuń funkcje od końca do początku (żeby indeksy się nie przesuwały)
total_removed = 0
for func_name, start, end in FUNCTIONS_TO_REMOVE:
    # Konwertuj na indeksy (Python używa 0-based, edytor 1-based)
    start_idx = start - 1
    end_idx = end  # end już jest inclusive w naszych zakresach
    
    # Usuń linie
    removed_count = end_idx - start_idx
    del lines[start_idx:end_idx]
    total_removed += removed_count
    print(f"  Usunięto {func_name}: linie {start}-{end} ({removed_count} linii)")

# Zapisz
with open('views/business_games.py', 'w', encoding='utf-8', newline='\n') as f:
    f.writelines(lines)

print(f"\n✅ Nowy plik: {len(lines)} linii")
print(f"✅ Usunięto łącznie: {total_removed} linii")
print(f"✅ Encoding: UTF-8 zachowany")

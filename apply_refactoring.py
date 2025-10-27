#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Skrypt do zastosowania refaktoryzacji KROK 1-4 z zachowaniem polskich znaków
"""

def apply_refactoring():
    # Wczytaj plik z UTF-8
    with open('views/business_games.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 1. Dodaj importy po istniejących importach (około linii 20-30)
    imports_to_add = """
# =============================================================================
# IMPORTY Z REFAKTORYZACJI
# =============================================================================
from views.business_games_refactored.helpers import (
    calculate_financial_impact as _calculate_financial_impact,
    calculate_reputation_change as _calculate_reputation_change,
    get_random_event as _get_random_event,
    trigger_bonus_event as _trigger_bonus_event,
    calculate_replay_value as _calculate_replay_value
)
from views.business_games_refactored.components.charts import (
    create_financial_chart as _create_financial_chart
)
from views.business_games_refactored.components.headers import (
    render_header as _render_header,
    render_fmcg_header as _render_fmcg_header
)
from views.business_games_refactored.components.event_card import (
    render_active_effects_badge as _render_active_effects_badge,
    render_latest_event_card as _render_latest_event_card,
    show_active_event_card as _show_active_event_card
)
from views.business_games_refactored.components.contract_card import (
    render_active_contract_card as _render_active_contract_card,
    render_decision_tree_contract as _render_decision_tree_contract,
    render_conversation_contract as _render_conversation_contract,
    render_speed_challenge_contract as _render_speed_challenge_contract,
    render_contract_card as _render_contract_card,
    render_completed_contract_card as _render_completed_contract_card
)

"""
    
    # Znajdź miejsce do wstawienia (po ostatnim imporcie, przed pierwszą funkcją)
    insert_pos = None
    for i, line in enumerate(lines):
        if line.startswith('def ') and not line.startswith('def __'):
            insert_pos = i
            break
    
    if insert_pos is None:
        # Jeśli nie znaleziono funkcji, wstaw po importach
        for i, line in enumerate(lines):
            if i > 10 and line.strip() == '' and not lines[i+1].startswith('import') and not lines[i+1].startswith('from'):
                insert_pos = i + 1
                break
    
    # Wstaw importy
    lines.insert(insert_pos, imports_to_add)
    
    # 2. Dodaj aliasy (zaraz po importach)
    aliases = """
# =============================================================================
# ALIASY DLA BACKWARD COMPATIBILITY
# =============================================================================
calculate_financial_impact = _calculate_financial_impact
calculate_reputation_change = _calculate_reputation_change
get_random_event = _get_random_event
trigger_bonus_event = _trigger_bonus_event
calculate_replay_value = _calculate_replay_value
create_financial_chart = _create_financial_chart
render_header = _render_header
render_fmcg_header = _render_fmcg_header
render_active_effects_badge = _render_active_effects_badge
render_latest_event_card = _render_latest_event_card
show_active_event_card = _show_active_event_card
render_active_contract_card = _render_active_contract_card
render_decision_tree_contract = _render_decision_tree_contract
render_conversation_contract = _render_conversation_contract
render_speed_challenge_contract = _render_speed_challenge_contract
render_contract_card = _render_contract_card
render_completed_contract_card = _render_completed_contract_card

"""
    
    lines.insert(insert_pos + 1, aliases)
    
    # 3. Znajdź i usuń stare definicje funkcji
    content = ''.join(lines)
    
    # Znajdź pozycje funkcji do usunięcia
    functions_to_remove = [
        'def calculate_financial_impact(',
        'def calculate_reputation_change(',
        'def get_random_event(',
        'def trigger_bonus_event(',
        'def calculate_replay_value(',
        'def create_financial_chart(',
        'def render_header(',
        'def render_fmcg_header(',
        'def render_active_effects_badge(',
        'def render_latest_event_card(',
        'def show_active_event_card(',
        'def render_active_contract_card(',
        'def render_decision_tree_contract(',
        'def render_conversation_contract(',
        'def render_speed_challenge_contract(',
        'def render_contract_card(',
        'def render_completed_contract_card(',
    ]
    
    # Podziel na linie ponownie
    lines = content.split('\n')
    
    # Znajdź zakresy do usunięcia
    ranges_to_remove = []
    for func_name in functions_to_remove:
        for i, line in enumerate(lines):
            if func_name in line and line.strip().startswith('def '):
                # Znajdź koniec funkcji (następna funkcja def lub koniec pliku)
                end = None
                indent_level = len(line) - len(line.lstrip())
                for j in range(i + 1, len(lines)):
                    next_line = lines[j]
                    if next_line.strip() and not next_line.startswith('#'):
                        next_indent = len(next_line) - len(next_line.lstrip())
                        if next_indent <= indent_level and (next_line.strip().startswith('def ') or next_line.strip().startswith('class ')):
                            end = j
                            break
                
                if end is None:
                    end = len(lines)
                
                ranges_to_remove.append((i, end))
                break
    
    # Sortuj zakresy od końca, żeby usuwanie nie psuło indeksów
    ranges_to_remove.sort(reverse=True)
    
    # Usuń funkcje
    for start, end in ranges_to_remove:
        del lines[start:end]
    
    # Zapisz z UTF-8
    final_content = '\n'.join(lines)
    with open('views/business_games.py', 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"✅ Refaktoryzacja zastosowana!")
    print(f"✅ Usunięto {len(ranges_to_remove)} funkcji")
    print(f"✅ Nowa długość pliku: {len(lines)} linii")

if __name__ == '__main__':
    apply_refactoring()

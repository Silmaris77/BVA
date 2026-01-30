#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cleanup: Usuwa stare definicje funkcji z business_games.py
Zachowuje UTF-8 encoding i polskie znaki
"""

import re

# Lista funkcji do usunięcia (te które zostały wyodrębnione do modułów)
FUNCTIONS_TO_REMOVE = [
    # helpers.py
    'get_contract_reward_coins',
    'get_contract_reward_reputation',
    'get_game_data',
    'save_game_data',
    'play_coin_sound',
    # charts.py
    'create_financial_chart',
    # headers.py
    'render_header',
    'render_fmcg_header',
    # event_card.py
    'render_active_effects_badge',
    'render_latest_event_card',
    'show_active_event_card',
    # contract_card.py
    'render_active_contract_card',
    'render_decision_tree_contract',
    'render_conversation_contract',
    'render_speed_challenge_contract',
    'render_contract_card',
    'render_completed_contract_card',
    # employee_card.py
    'render_employee_card',
    'render_hire_card',
]

def find_function_range(lines, func_name, start_search=0):
    """Znajduje zakres linii dla danej funkcji"""
    pattern = rf'^def {re.escape(func_name)}\('
    
    for i in range(start_search, len(lines)):
        if re.match(pattern, lines[i]):
            # Znaleziono początek funkcji
            indent = len(lines[i]) - len(lines[i].lstrip())
            
            # Znajdź koniec funkcji
            for j in range(i + 1, len(lines)):
                line = lines[j]
                
                # Pomiń puste linie i komentarze
                if not line.strip() or line.strip().startswith('#'):
                    continue
                
                # Sprawdź wcięcie
                line_indent = len(line) - len(line.lstrip())
                
                # Jeśli trafimy na def/class na tym samym lub mniejszym wcięciu, to koniec
                if line_indent <= indent and (line.strip().startswith('def ') or 
                                               line.strip().startswith('class ') or
                                               line.strip().startswith('@')):
                    return i, j
            
            # Jeśli nie znaleziono końca, funkcja trwa do końca pliku
            return i, len(lines)
    
    return None, None

def remove_old_functions(filepath):
    """Usuwa stare funkcje zachowując UTF-8"""
    
    print(f"📖 Wczytuję {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    original_count = len(lines)
    print(f"   Oryginalny rozmiar: {original_count} linii\n")
    
    # Znajdź wszystkie zakresy funkcji do usunięcia
    ranges_to_remove = []
    
    for func_name in FUNCTIONS_TO_REMOVE:
        start, end = find_function_range(lines, func_name)
        if start is not None:
            ranges_to_remove.append((func_name, start, end))
            print(f"   ✓ Znaleziono {func_name}: linie {start+1}-{end}")
        else:
            print(f"   ⚠ Nie znaleziono {func_name} (może już usunięta)")
    
    if not ranges_to_remove:
        print("\n⚠ Nie znaleziono funkcji do usunięcia!")
        return False
    
    # Sortuj od końca, żeby usuwanie nie psuło indeksów
    ranges_to_remove.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n🗑️ Usuwam {len(ranges_to_remove)} funkcji...\n")
    
    total_removed = 0
    for func_name, start, end in ranges_to_remove:
        lines_removed = end - start
        del lines[start:end]
        total_removed += lines_removed
        print(f"   ✓ Usunięto {func_name}: {lines_removed} linii")
    
    # Zapisz z UTF-8
    print(f"\n💾 Zapisuję plik...")
    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(lines)
    
    new_count = len(lines)
    reduction = ((original_count - new_count) / original_count) * 100
    
    print(f"\n✅ CLEANUP ZAKOŃCZONY!")
    print(f"   Przed: {original_count} linii")
    print(f"   Po:    {new_count} linii")
    print(f"   Usunięto: {total_removed} linii ({reduction:.1f}% redukcja)")
    print(f"   Encoding: UTF-8 ✓")
    
    return True

if __name__ == '__main__':
    success = remove_old_functions('views/business_games.py')
    if not success:
        exit(1)

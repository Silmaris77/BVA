import sys

with open('views/tools.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Znajdź linię z st.tabs i zamień kolejność
new_lines = []
tabs_found = False

for i, line in enumerate(lines):
    if 'tab1, tab2, tab3, tab4, tab5 = st.tabs([' in line and not tabs_found:
        # Następne 5 linii to nazwy zakładek
        new_lines.append(line)
        tabs_found = True
        
        # Zbierz 5 kolejnych linii (nazwy zakładek)
        tab_lines = []
        for j in range(i+1, min(i+6, len(lines))):
            tab_lines.append(lines[j])
        
        # Znajdź indeksy
        autodiagnoza_idx = None
        for idx, tab_line in enumerate(tab_lines):
            if 'Autodiagnoza' in tab_line:
                autodiagnoza_idx = idx
                break
        
        # Przesuń Autodiagnozę na początek
        if autodiagnoza_idx is not None:
            autodiagnoza_line = tab_lines.pop(autodiagnoza_idx)
            # Usuń przecinek z ostatniej linii i dodaj do Autodiagnoza
            if autodiagnoza_line.rstrip().endswith('\"'):
                autodiagnoza_line = autodiagnoza_line.rstrip() + ',\n'
            tab_lines.insert(0, autodiagnoza_line)
            
            # Usuń przecinek z nowej ostatniej linii
            if tab_lines[-1].rstrip().endswith(','):
                tab_lines[-1] = tab_lines[-1].rstrip()[:-1] + '\n'
        
        # Dodaj przetasowane linie
        new_lines.extend(tab_lines)
        
        # Pomiń oryginalne linie zakładek
        for _ in range(len(tab_lines)):
            next(enumerate(lines))
            
    elif tabs_found and i <= i + len(tab_lines):
        # Pomiń linie które już przetwarzaliśmy
        tabs_found = False
        continue
    else:
        new_lines.append(line)

# Zapisz
with open('views/tools.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Tabs order changed successfully!")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Extract FMCG module from business_games.py"""

import os

# Utwórz katalog industries jeśli nie istnieje
os.makedirs('views/business_games_refactored/industries', exist_ok=True)

# Wyodrębnij sekcję FMCG (linie 871-2058)
with open('views/business_games.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Linie 871-2058 (0-based: 870-2057)
fmcg_lines = lines[870:2058]

# Dodaj header
header = '''"""
🛒 FMCG Industry Module for Business Games

Moduł branży FMCG (Fast-Moving Consumer Goods) - FreshLife Poland
Zawiera wszystkie zakładki i funkcjonalności specyficzne dla FMCG.

Wyekstrahowane z business_games.py (KROK 7 - FMCG separation)
"""

import streamlit as st
from datetime import datetime
from views.business_games_refactored.helpers import get_game_data, save_game_data

'''

content = header + ''.join(fmcg_lines)

with open('views/business_games_refactored/industries/fmcg.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'✅ Utworzono fmcg.py: {len(fmcg_lines)} linii + header ({len(content.splitlines())} total)')

# Utwórz __init__.py
with open('views/business_games_refactored/industries/__init__.py', 'w', encoding='utf-8') as f:
    f.write('')

print('✅ Utworzono __init__.py')

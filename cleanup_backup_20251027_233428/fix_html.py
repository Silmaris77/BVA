# -*- coding: utf-8 -*-
"""Zamieniaj ?? w raportach HTML"""

with open('views/tools.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Zamień ?? w HTML
html_replacements = {
    '<h1>?? ': '<h1>📊 ',
    '<h2 class="section-title">?? ': '<h2 class="section-title">📋 ',
    '<h3 style="color: #2ECC71;">?? ': '<h3 style="color: #2ECC71;">💪 ',
    '<h3 style="color: #E67E22;">?? ': '<h3 style="color: #E67E22;">🎯 ',
    '<h3 style="color: #3498DB;">?? ': '<h3 style="color: #3498DB;">👔 ',
    '<h3 style="color: #9B59B6;">?? ': '<h3 style="color: #9B59B6;">📚 ',
    '{"?? ': '{"✅ ',
}

for old, new in html_replacements.items():
    content = content.replace(old, new)

with open('views/tools.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Naprawiono ?? w raportach HTML')

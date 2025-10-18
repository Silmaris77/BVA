# -*- coding: utf-8 -*-
"""Napraw pozostałe emoji w tools.py - część 2"""

with open('views/tools.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Dodatkowe zamiany
replacements = {
    # Expandery z poziomami
    'with st.expander("?? Poziom I - Transakcyjny"': 'with st.expander("🔴 Poziom I - Transakcyjny"',
    'with st.expander("?? Poziom II - Pozycyjny"': 'with st.expander("🟡 Poziom II - Pozycyjny"',
    'with st.expander("?? Poziom III - Transformacyjny"': 'with st.expander("🟢 Poziom III - Transformacyjny"',
    
    # Markdown z poziomami
    'st.markdown("**?? Poziom I - Transakcyjny**")': 'st.markdown("**🔴 Poziom I - Transakcyjny**")',
    'st.markdown("**?? Poziom II - Pozycyjny**")': 'st.markdown("**🟡 Poziom II - Pozycyjny**")',
    'st.markdown("**?? Poziom III - Transformacyjny**")': 'st.markdown("**🟢 Poziom III - Transformacyjny**")',
    
    # Zakładki i tematy
    '"?? Dynamika Zespołu"': '"👥 Dynamika Zespołu"',
    '"?? Sygnały Problemów"': '"⚠️ Sygnały Problemów"',
    '"?? Leadership Coach"': '"🎓 Leadership Coach"',
    
    # Teksty i prompty
    '"?? Wklej transkrypcję rozmowy menedżerskiej:"': '"📝 Wklej transkrypcję rozmowy menedżerskiej:"',
    '"?? Analizuj Sentiment + C-IQ"': '"🔍 Analizuj Sentiment + C-IQ"',
    '"?? Analizuję sentiment i poziomy C-IQ..."': '"🔍 Analizuję sentiment i poziomy C-IQ..."',
    '"?? Wykryj Intencje"': '"🎯 Wykryj Intencje"',
    '"?? Tekst do analizy sygnałów problemów:"': '"⚠️ Tekst do analizy sygnałów problemów:"',
    
    # Wyniki analizy
    'st.markdown("**?? Wykrywane potrzeby pracownika:**")': 'st.markdown("**💡 Wykrywane potrzeby pracownika:**")',
    'st.markdown("**?? Wyniki analizy:**")': 'st.markdown("**📊 Wyniki analizy:**")',
    'st.markdown("**?? Sygnały eskalacji:**")': 'st.markdown("**⚠️ Sygnały eskalacji:**")',
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open('views/tools.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Naprawiono pozostałe emoji w tools.py - część 2')

#!/usr/bin/env python
# -*- coding: utf-8 -*-

with open('views/tools.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Zamień kolejność zakładek - prosta zamiana stringów
content = content.replace(
    '''    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🧠 C-IQ Tools", 
        "🎭 Symulatory", 
        "📊 Analityki", 
        "🤖 AI Asystent",
        "🎯 Autodiagnoza"
    ])''',
    '''    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Autodiagnoza",
        "🧠 C-IQ Tools", 
        "🎭 Symulatory", 
        "📊 Analityki", 
        "🤖 AI Asystent"
    ])'''
)

# Zamień też wywołania funkcji
content = content.replace(
    '''    with tab1:
        show_ciq_tools()
    
    with tab2:
        show_simulators()
    
    with tab3:
        show_analytics()
        
    with tab4:
        show_ai_assistant()
    
    with tab5:
        show_autodiagnosis()''',
    '''    with tab1:
        show_autodiagnosis()
    
    with tab2:
        show_ciq_tools()
    
    with tab3:
        show_simulators()
    
    with tab4:
        show_analytics()
        
    with tab5:
        show_ai_assistant()'''
)

# Zaktualizuj info message
content = content.replace(
    'st.info("💡 Przejdź do zakładki **🎯 Autodiagnoza** aby zobaczyć lub wykonać testy diagnostyczne")',
    'st.info("💡 Jesteś w zakładce **🎯 Autodiagnoza** - pierwsza zakładka poniżej")'
)

with open('views/tools.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Tabs order changed successfully!")

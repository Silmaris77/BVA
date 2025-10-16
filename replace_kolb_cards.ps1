$file = "c:\Users\pksia\Dropbox\BVA\views\tools.py"
$content = Get-Content $file -Encoding UTF8 -Raw

$old = @"
    # Dodatkowe informacje o cyklu Kolba i elastyczności
    st.markdown("---")
    st.markdown("### 🔄 Strategia rozwoju elastyczności uczenia się")
    
    # Identyfikacja słabych zdolności
    weak_abilities = [ability for ability, score in results.items() if score < 4]
    strong_abilities = [ability for ability, score in results.items() if score > 8]
    
    if weak_abilities:
        st.markdown("#### 🎯 Zdolności do wzmocnienia:")
        st.info(f"""
        Twoje słabsze zdolności to: **{', '.join([ability_info[a]['name'] for a in weak_abilities])}**
        
        💡 **Zalecenia rozwojowe**: Celowo angażuj się w sytuacje, które wymagają używania tych zdolności. 
        Na przykład: {' '.join([f"• Dla {ability_info[a]['name']} ({a}): ćwicz {ability_info[a]['desc'].lower()}" for a in weak_abilities])}
        """)
    
    st.markdown("""
    ### 📊 Pełny Cykl Uczenia się Kolba (ELT Cycle)
    
    Najbardziej efektywne uczenie się wykorzystuje **wszystkie cztery fazy** w cyklu:
    
    1. **Konkretne Doświadczenie (CE)** → Zetknięcie się z nową sytuacją (Feeling)
    2. **Refleksyjna Obserwacja (RO)** → Obserwacja i refleksja (Watching)
    3. **Abstrakcyjna Konceptualizacja (AC)** → Tworzenie teorii (Thinking)
    4. **Aktywne Eksperymentowanie (AE)** → Testowanie w praktyce (Doing)
    
    💡 **Kluczowa wskazówka**: Twój wynik elastyczności ({flexibility:.0f}%) pokazuje, jak dobrze potrafisz przełączać się 
    między stylami. {"Im bliżej centrum siatki, tym większa zdolność adaptacji do różnych sytuacji uczenia się." if flexibility > 50 else "Rozwijaj słabsze zdolności, aby zwiększyć elastyczność i efektywność uczenia się w różnych kontekstach."}
    """)
"@

$new = @'
    # Karta ze strategią rozwoju elastyczności
    st.markdown("---")
    
    # Identyfikacja słabych zdolności
    weak_abilities = [ability for ability, score in results.items() if score < 4]
    strong_abilities = [ability for ability, score in results.items() if score > 8]
    
    if weak_abilities:
        weak_abilities_names = ', '.join([ability_info[a]['name'] for a in weak_abilities])
        weak_tips_html = "<br>".join([f"• Dla <b>{ability_info[a]['name']} ({a})</b>: ćwicz {ability_info[a]['desc'].lower()}" for a in weak_abilities])
        
        st.markdown(f"""
        <div style='background: linear-
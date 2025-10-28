# Skrypt do poprawy wizualizacji testu Kolba
$file = "c:\Users\pksia\Dropbox\BVA\views\tools.py"
$content = Get-Content $file -Encoding UTF8 -Raw

# 1. INSTRUKCJA - zamień stary markdown na karty z gradientami
$old1 = @"
def show_kolb_test():
    """Wyświetla test stylów uczenia się według Kolba"""
    st.markdown("### 🔄 Kolb Experiential Learning Profile (KELP)")
    st.markdown("""
    **Teoria Uczenia się przez Doświadczenie (ELT)** Davida Kolba z 1984 roku definiuje uczenie się jako 
    dynamiczny proces, w którym wiedza jest tworzona poprzez transformację doświadczenia.
    
    #### Cykl Uczenia się Kolba składa się z czterech faz:
    
    1. **Konkretne Doświadczenie (CE)** → Zetknięcie się z nową sytuacją (Feeling)
    2. **Refleksyjna Obserwacja (RO)** → Obserwacja i refleksja nad doświadczeniem (Watching)
    3. **Abstrakcyjna Konceptualizacja (AC)** → Tworzenie teorii i uogólnień (Thinking)
    4. **Aktywne Eksperymentowanie (AE)** → Testowanie koncepcji w praktyce (Doing)
    
    #### Wymiary biegunowe:
    - **Oś Postrzegania**: Konkretne Przeżycie (CE) ↔ Abstrakcyjna Konceptualizacja (AC)
    - **Oś Przetwarzania**: Refleksyjna Obserwacja (RO) ↔ Aktywne Eksperymentowanie (AE)
    
    💡 **Cel testu**: Zidentyfikować Twój preferowany styl uczenia się i ocenić elastyczność w przechodzeniu 
    przez pełny cykl Kolba.
    """)
"@

$new1 = @'
def show_kolb_test():
    """Wyświetla test stylów uczenia się według Kolba"""
    st.markdown("### 🔄 Kolb Experiential Learning Profile (KELP)")
    
    # Karta z teorią ELT
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                box-shadow: 0 4px 15px rgba(102,126,234,0.4); 
                border-radius: 20px; 
                padding: 30px; 
                margin: 20px 0; 
                color: white;'>
        <div style='font-size: 2.5em; margin-bottom: 15px;'>📚</div>
        <h4 style='color: white; margin: 0 0 20px 0;'>Teoria Uczenia się przez Doświadczenie (ELT)</h4>
        <p style='font-size: 1.1em; line-height: 1.7; margin-bottom: 0;'>
            Teoria Davida Kolba z 1984 roku definiuje uczenie się jako <b>dynamiczny proces</b>, 
            w którym wiedza jest tworzona poprzez <b>transformację doświadczenia</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Karty z czterema fazami cyklu
    st.markdown("<h4 style='margin: 30px 0 20px 0; color: #333;'>🔄 Cykl Uczenia się Kolba - Cztery Fazy:</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%); 
                    box-shadow: 0 3px 10px rgba(231,76,60,0.3); 
                    border-radius: 15px; 
                    padding: 20px; 
                    margin: 10px 0; 
                    color: white;'>
            <div style='font-size: 2em; margin-bottom: 10px;'>❤️</div>
            <h5 style='color: white; margin: 0 0 10px 0;'>1. Konkretne Doświadczenie (CE)</h5>
            <p style='margin: 0; font-size: 0.95em; line-height: 1.6;'>
                Zetknięcie się z nową sytuacją<br><b>→ Feeling (Odczuwanie)</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, #9B59B6 0%, #8E44AD 100%); 
                    box-shadow: 0 3px 10px rgba(155,89,182,0.3); 
                    border-radius: 15px; 
                    padding: 20px; 
                    margin: 10px 0; 
                    color: white;'>
            <div style='font-size: 2em; margin-bottom: 10px;'>🧠</div>
            <h5 style='color: white; margin: 0 0 10px 0;'>3. Abstrakcyjna Konceptualizacja (AC)</h5>
            <p style='margin: 0; font-size: 0.95em; line-height: 1.6;'>
                Tworzenie teorii i uogólnień<br><b>→ Thinking (Myślenie)</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%); 
                    box-shadow: 0 3px 10px rgba(74,144,226,0.3); 
                    border-radius: 15px; 
                    padding: 20px; 
                    margin: 10px 0; 
                    color: white;'>
            <div style='font-size: 2em; margin-bottom: 10px;'>👁️</div>
            <h5 style='color: white; margin: 0 0 10px 0;'>2. Refleksyjna Obserwacja (RO)</h5>
            <p style='margin: 0; font-size: 0.95em; line-height: 1.6;'>
                Obserwacja i refleksja<br><b>→ Watching (Obserwowanie)</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%); 
                    box-shadow: 0 3px 10px rgba(46,204,113,0.3); 
                    border-radius: 15px; 
                    padding: 20px; 
                    margin: 10px 0; 
                    color: white;'>
            <div style='font-size: 2em; margin-bottom: 10px;'>⚙️</div>
            <h5 style='color: white; margin: 0 0 10px 0;'>4. Aktywne Eksperymentowanie (AE)</h5>
            <p style='margin: 0; font-size: 0.95em; line-height: 1.6;'>
                Testowanie koncepcji w praktyce<br><b>→ Doing (Działanie)</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Karta z wymiarami biegunowymi
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                box-shadow: 0 3px 12px rgba(240,147,251,0.4); 
                border-radius: 18px; 
                padding: 25px; 
                margin: 25px 0; 
                color: white;'>
        <div style='font-size: 2em; margin-bottom: 10px;'>⚖️</div>
        <h5 style='color: white; margin: 0 0 15px 0;'>Wymiary Biegunowe:</h5>
        <ul style='margin: 0; padding-left: 20px; line-height: 2;'>
            <li><b>Oś Postrzegania:</b> Konkretne Przeżycie (CE) ↔ Abstrakcyjna Konceptualizacja (AC)</li>
            <li><b>Oś Przetwarzania:</b> Refleksyjna Obserwacja (RO) ↔ Aktywne Eksperymentowanie (AE)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Karta z celem testu
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%); 
                box-shadow: 0 3px 10px rgba(255,234,167,0.3); 
                border-radius: 15px; 
                padding: 20px; 
                margin: 20px 0; 
                color: #222;'>
        <div style='font-size: 2em; margin-bottom: 10px;'>🎯</div>
        <h5 style='margin: 0 0 10px 0; color: #e17055;'>Cel testu:</h5>
        <p style='margin: 0; font-size: 1.05em; line-height: 1.7;'>
            Zidentyfikować Twój <b>preferowany styl uczenia się</b> i ocenić <b>elastyczność</b> 
            w przechodzeniu przez pełny cykl Kolba.
        </p>
    </div>
    """, unsafe_allow_html=True)
'@

Write-Host "Krok 1: Zastępuję sekcję instrukcji..." -ForegroundColor Yellow
$content = $content.Replace($old1, $new1)

# 2. PYTANIA - zamień stary markdown na karty
$old2 = @"
    # Wyświetl pytania
    st.markdown("---")
    st.markdown("#### Odpowiedz na poniższe pytania, wybierając opcję najbardziej do Ciebie pasującą:")
    
    for q in questions:
        st.markdown(f"**{q['id']}. {q['question']}**")
        answer = st.radio(
            f"Pytanie {q['id']}",
            options=list(q['options'].keys()),
            format_func=lambda x, opts=q['options']: opts[x],
            key=f"kolb_q{q['id']}",
            label_visibility="collapsed"
        )
        st.session_state.kolb_answers[q['id']] = answer
        st.markdown("")
"@

$new2 = @'
    # Wyświetl pytania
    st.markdown("---")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                border-radius: 12px; 
                padding: 15px; 
                margin: 20px 0; 
                text-align: center;'>
        <h4 style='margin: 0; color: #2c3e50;'>📝 Odpowiedz na poniższe pytania</h4>
        <p style='margin: 5px 0 0 0; color: #555;'>Wybierz opcję najbardziej do Ciebie pasującą</p>
    </div>
    """, unsafe_allow_html=True)
    
    for q in questions:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                    border-left: 5px solid #3498db; 
                    border-radius: 10px; 
                    padding: 20px; 
                    margin: 15px 0; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <h5 style='margin: 0 0 15px 0; color: #2c3e50;'>
                <span style='background: #3498db; color: white; padding: 5px 12px; border-radius: 50%; margin-right: 10px;'>{q['id']}</span>
                {q['question']}
            </h5>
        </div>
        """, unsafe_allow_html=True)
        
        answer = st.radio(
            f"Pytanie {q['id']}",
            options=list(q['options'].keys()),
            format_func=lambda x, opts=q['options']: opts[x],
            key=f"kolb_q{q['id']}",
            label_visibility="collapsed"
        )
        st.session_state.kolb_answers[q['id']] = answer
        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
'@

Write-Host "Krok 2: Zastępuję sekcję pytań..." -ForegroundColor Yellow
$content = $content.Replace($old2, $new2)

# 3. WYNIKI - zamień sekcję opisów stylu na karty
$old3 = @"
    desc = style_descriptions[dominant]
    
    st.markdown(f"**{desc['description']}**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💪 Twoje mocne strony:")
        for strength in desc['strengths']:
            st.markdown(f"✅ {strength}")
        
        st.markdown("#### 🎯 Typowe zawody:")
        st.markdown(f"💼 {desc['careers']}")
    
    with col2:
        st.markdown("#### ⚠️ Obszary do rozwoju:")
        for weakness in desc['weaknesses']:
            st.markdown(f"� {weakness}")
        
        st.markdown("#### 📚 Rekomendowane metody szkoleniowe:")
        st.markdown(f"🎓 {desc['learning_methods']}")
"@

$new3 = @'
    desc = style_descriptions[dominant]
    
    # Główna karta z opisem stylu
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                box-shadow: 0 4px 15px rgba(102,126,234,0.4); 
                border-radius: 20px; 
                padding: 30px; 
                margin: 25px 0; 
                color: white;'>
        <div style='font-size: 2.5em; margin-bottom: 10px;'>🎯</div>
        <h4 style='color: white; margin: 0 0 15px 0;'>Twój Styl Uczenia się</h4>
        <p style='font-size: 1.15em; line-height: 1.8; margin: 0;'>
            {desc['description']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Szczegółowe karty w 2 kolumnach
    col1, col2 = st.columns(2)
    
    with col1:
        # Karta mocnych stron
        strengths_html = "<br>".join([f"✅ {s}" for s in desc['strengths']])
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%); 
                    box-shadow: 0 3px 12px rgba(46,204,113,0.3); 
                    border-radius: 18px; 
                    padding: 25px; 
                    margin: 15px 0; 
                    color: white;'>
            <div style='font-size: 2em; margin-bottom: 10px;'>💪</div>
            <h4 style='margin: 0 0 15px 0; color: white;'>Twoje mocne strony</h4>
            <p style='margin: 0; font-size: 1.05em; line-height: 1.8;'>{strengths_html}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Karta zawodów
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); 
                    box-shadow: 0 3px 12px rgba(52,152,219,0.3); 
                    border-radius: 18px; 
                    padding: 25px; 
                    margin: 15px 0; 
                    color: white;'>
            <div style='font-size: 2em; margin-bottom: 10px;'>💼</div>
            <h4 style='margin: 0 0 15px 0; color: white;'>Typowe zawody</h4>
            <p style='margin: 0; font-size: 1.05em; line-height: 1.7;'>{desc['careers']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Karta obszarów rozwoju
        weaknesses_html = "<br>".join([f"⚠️ {w}" for w in desc['weaknesses']])
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #e67e22 0%, #d35400 100%); 
                    box-shadow: 0 3px 12px rgba(230,126,34,0.3); 
                    border-radius: 18px; 
                    padding: 25px; 
                    margin: 15px 0; 
                    color: white;'>
            <div style='font-size: 2em; margin-bottom: 10px;'>🎯</div>
            <h4 style='margin: 0 0 15px 0; color: white;'>Obszary do rozwoju</h4>
            <p style='margin: 0; font-size: 1.05em; line-height: 1.8;'>{weaknesses_html}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Karta metod szkoleniowych
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); 
                    box-shadow: 0 3px 12px rgba(155,89,182,0.3); 
                    border-radius: 18px; 
                    padding: 25px; 
                    margin: 15px 0; 
                    color: white;'>
            <div style='font-size: 2em; margin-bottom: 10px;'>📚</div>
            <h4 style='margin: 0 0 12px 0; color: white;'>Rekomendowane metody szkoleniowe</h4>
            <p style='margin: 0; font-size: 1.05em; line-height: 1.6;'>{desc['learning_methods']}</p>
        </div>
        """, unsafe_allow_html=True)
'@

Write-Host "Krok 3: Zastępuję sekcję opisów stylu..." -ForegroundColor Yellow
$content = $content.Replace($old3, $new3)

# 4. SEKCJA ROZWOJU ELASTYCZNOŚCI - zamień na karty
$old4 = @"
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

$new4 = @'
    # Karta ze strategią rozwoju elastyczności
    st.markdown("---")
    
    # Identyfikacja słabych zdolności
    weak_abilities = [ability for ability, score in results.items() if score < 4]
    strong_abilities = [ability for ability, score in results.items() if score > 8]
    
    if weak_abilities:
        weak_abilities_names = ', '.join([ability_info[a]['name'] for a in weak_abilities])
        weak_tips_html = "<br>".join([f"• Dla <b>{ability_info[a]['name']} ({a})</b>: ćwicz {ability_info[a]['desc'].lower()}" for a in weak_abilities])
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%); 
                    box-shadow: 0 3px 12px rgba(255,234,167,0.3); 
                    border-radius: 18px; 
                    padding: 25px; 
                    margin: 20px 0; 
                    color: #222;'>
            <div style='font-size: 2em; margin-bottom: 10px;'>🎯</div>
            <h4 style='margin: 0 0 15px 0; color: #e17055;'>Zdolności do wzmocnienia</h4>
            <p style='margin: 0 0 15px 0; font-size: 1.05em;'>
                Twoje słabsze zdolności to: <b>{weak_abilities_names}</b>
            </p>
            <div style='background: rgba(255,255,255,0.3); 
                        border-radius: 10px; 
                        padding: 15px; 
                        margin-top: 15px;'>
                <p style='margin: 0 0 10px 0; font-weight: bold;'>💡 Zalecenia rozwojowe:</p>
                <p style='margin: 0; line-height: 1.8;'>
                    Celowo angażuj się w sytuacje, które wymagają używania tych zdolności:<br><br>
                    {weak_tips_html}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Karta z pełnym cyklem Kolba
    flexibility_message = "Im bliżej centrum siatki, tym większa zdolność adaptacji do różnych sytuacji uczenia się." if flexibility > 50 else "Rozwijaj słabsze zdolności, aby zwiększyć elastyczność i efektywność uczenia się w różnych kontekstach."
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                box-shadow: 0 4px 15px rgba(102,126,234,0.4); 
                border-radius: 20px; 
                padding: 30px; 
                margin: 20px 0; 
                color: white;'>
        <div style='font-size: 2em; margin-bottom: 10px;'>🔄</div>
        <h4 style='color: white; margin: 0 0 20px 0;'>Pełny Cykl Uczenia się Kolba (ELT Cycle)</h4>
        <p style='font-size: 1.05em; line-height: 1.7; margin-bottom: 20px;'>
            Najbardziej efektywne uczenie się wykorzystuje <b>wszystkie cztery fazy</b> w cyklu:
        </p>
        <div style='background: rgba(255,255,255,0.15); 
                    border-radius: 12px; 
                    padding: 20px; 
                    margin: 15px 0;'>
            <ol style='margin: 0; padding-left: 20px; line-height: 2;'>
                <li><b>Konkretne Doświadczenie (CE)</b> → Zetknięcie się z nową sytuacją (Feeling)</li>
                <li><b>Refleksyjna Obserwacja (RO)</b> → Obserwacja i refleksja (Watching)</li>
                <li><b>Abstrakcyjna Konceptualizacja (AC)</b> → Tworzenie teorii (Thinking)</li>
                <li><b>Aktywne Eksperymentowanie (AE)</b> → Testowanie w praktyce (Doing)</li>
            </ol>
        </div>
        <div style='background: rgba(255,193,7,0.3); 
                    border-left: 4px solid #FFC107; 
                    border-radius: 8px; 
                    padding: 15px; 
                    margin-top: 20px;'>
            <p style='margin: 0; font-size: 1.05em;'>
                <b>💡 Kluczowa wskazówka:</b> Twój wynik elastyczności (<b>{flexibility:.0f}%</b>) pokazuje, 
                jak dobrze potrafisz przełączać się między stylami. {flexibility_message}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
'@

Write-Host "Krok 4: Zastępuję sekcję rozwoju elastyczności..." -ForegroundColor Yellow
$content = $content.Replace($old4, $new4)

# Zapisz zmieniony plik
Write-Host "Zapisuję zmiany..." -ForegroundColor Green
$content | Set-Content $file -Encoding UTF8

Write-Host "✅ Wizualizacja testu Kolba została poprawiona!" -ForegroundColor Green
Write-Host "Zmiany:" -ForegroundColor Cyan
Write-Host "  - Instrukcja: Karty z gradientami dla teorii ELT" -ForegroundColor White
Write-Host "  - Pytania: Numerowane karty z kolorowym obramowaniem" -ForegroundColor White
Write-Host "  - Wyniki: Karty dla opisów stylu, mocnych stron, zawodów, metod" -ForegroundColor White
Write-Host "  - Rozwój: Karty dla słabych zdolności i cyklu ELT" -ForegroundColor White

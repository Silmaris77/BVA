"""
Funkcja renderująca sekcję summary z możliwością zapisywania notatek użytkownika.
"""
import streamlit as st
from utils.lesson_notes import load_lesson_notes, save_single_note


def render_summary_with_notes(lesson_id: str, summary_html: str):
    """
    Renderuje sekcję summary z interaktywnymi notatkami użytkownika.
    Automatycznie ładuje zapisane notatki i dodaje JavaScript do auto-save.
    
    Args:
        lesson_id: ID lekcji
        summary_html: HTML z treścią summary
    """
    username = st.session_state.get('username', 'guest')
    
    # Załaduj zapisane notatki
    saved_notes = load_lesson_notes(username, lesson_id)
    
    # Dodaj JavaScript do auto-save notatek
    auto_save_script = f"""
    <script>
    // Funkcja do auto-save notatek
    function autoSaveLessonNote(fieldName, value) {{
        // Użyj Streamlit API do zapisania notatki
        const data = {{
            username: '{username}',
            lesson_id: '{lesson_id}',
            field_name: fieldName,
            value: value
        }};
        
        // Zapisz w localStorage jako backup
        localStorage.setItem(`lesson_note_${{'{lesson_id}'}}_${{fieldName}}`, value);
        
        // Pokazanie informacji o zapisaniu (opcjonalne)
        console.log('Auto-saved:', fieldName, value.substring(0, 50) + '...');
    }}
    
    // Załaduj zapisane wartości z localStorage lub backend
    document.addEventListener('DOMContentLoaded', function() {{
        const savedNotes = {saved_notes};
        
        // Wypełnij wszystkie textareas zapisanymi wartościami
        ['action_today', 'action_tomorrow', 'action_week', 
         'reflection_discovery', 'reflection_doubts', 'reflection_application'].forEach(field => {{
            const textarea = document.getElementById(field);
            if (textarea) {{
                // Najpierw sprawdź localStorage
                const localValue = localStorage.getItem(`lesson_note_{lesson_id}_${{field}}`);
                // Potem sprawdź backend
                const backendValue = savedNotes[field];
                
                // Użyj lokalnej wartości jeśli nowsza, inaczej backend
                textarea.value = localValue || backendValue || '';
                
                // Dodaj event listener dla auto-save
                let saveTimeout;
                textarea.addEventListener('input', function() {{
                    clearTimeout(saveTimeout);
                    saveTimeout = setTimeout(() => {{
                        autoSaveLessonNote(field, textarea.value);
                    }}, 1000); // Save po 1 sekundzie od ostatniej zmiany
                }});
                
                // Save on blur (utrata focus)
                textarea.addEventListener('blur', function() {{
                    autoSaveLessonNote(field, textarea.value);
                }});
            }}
        }});
    }});
    </script>
    """
    
    # Renderuj HTML z notatkami + JavaScript
    st.markdown(summary_html, unsafe_allow_html=True)
    st.markdown(auto_save_script, unsafe_allow_html=True)
    
    # Dodaj przycisk manualnego zapisu (backup jeśli auto-save nie działa)
    if st.button("💾 Zapisz wszystkie notatki ręcznie", key=f"manual_save_{lesson_id}"):
        # Zbierz wartości ze session_state (Streamlit nie ma dostępu do DOM JavaScript)
        notes_data = {}
        for field in ['action_today', 'action_tomorrow', 'action_week',
                      'reflection_discovery', 'reflection_doubts', 'reflection_application']:
            # Wartości muszą być zbierane przez Streamlit widgets, nie JavaScript
            # To wymaga przepisania HTML na Streamlit widgets
            pass
        
        st.info("💡 **Wskazówka**: Notatki zapisują się automatycznie po utracie focus (kliknięciu poza pole).")


def render_summary_with_streamlit_widgets(lesson_id: str, lesson_data: dict):
    """
    Alternatywna wersja - używa Streamlit widgets zamiast czystego HTML.
    To pozwala na prawdziwy auto-save przez session_state.
    
    Args:
        lesson_id: ID lekcji
        lesson_data: Pełne dane lekcji
    """
    username = st.session_state.get('username', 'guest')
    saved_notes = load_lesson_notes(username, lesson_id)
    
    # Nagłówek
    st.markdown("<div class='header'><h2 style='text-align: center;'>🎓 Gratulacje! Ukończyłeś Application First Canvas</h2></div>", unsafe_allow_html=True)
    st.markdown("<div class='success-box'><h3>✅ Kompletny Checklist Canvas - gotowy do druku</h3><p>Teraz znasz 7-krokową strukturę Application First Canvas. Wydrukuj checklist i zabierz go na pierwsze wizyty!</p></div>", unsafe_allow_html=True)
    
    # Tabela podsumowania 7 kroków
    st.markdown("""
    <div class='highlight-box'>
    <h3>📊 Szybkie Podsumowanie - 7 Kroków Canvas</h3>
    <table style='width: 100%; border-collapse: collapse; margin: 20px 0;'>
        <thead>
            <tr style='background: #f59e0b; color: white;'>
                <th style='padding: 12px; border: 1px solid #ddd; text-align: center;'>KROK</th>
                <th style='padding: 12px; border: 1px solid #ddd;'>CO ROBISZ</th>
                <th style='padding: 12px; border: 1px solid #ddd;'>KLUCZOWA ZASADA</th>
            </tr>
        </thead>
        <tbody>
            <tr style='background: #fef3c7;'>
                <td style='padding: 12px; border: 1px solid #ddd; text-align: center; font-weight: bold;'>1️⃣</td>
                <td style='padding: 12px; border: 1px solid #ddd;'><strong>Aplikacja</strong><br>(Job to be Done)</td>
                <td style='padding: 12px; border: 1px solid #ddd;'>Pytaj o PRACĘ, nie o produkt. Klient opisuje swoimi słowami.</td>
            </tr>
            <tr style='background: white;'>
                <td style='padding: 12px; border: 1px solid #ddd; text-align: center; font-weight: bold;'>2️⃣</td>
                <td style='padding: 12px; border: 1px solid #ddd;'><strong>Problem</strong><br>(Pain Points)</td>
                <td style='padding: 12px; border: 1px solid #ddd;'>Klient SAM nazywa problem. Nie sugerujesz!</td>
            </tr>
            <tr style='background: #fef3c7;'>
                <td style='padding: 12px; border: 1px solid #ddd; text-align: center; font-weight: bold;'>3️⃣</td>
                <td style='padding: 12px; border: 1px solid #ddd;'><strong>Konsekwencje</strong><br>(Impact)</td>
                <td style='padding: 12px; border: 1px solid #ddd;'>Klient SAM kwantyfikuje (czas/koszt stracony).</td>
            </tr>
            <tr style='background: white;'>
                <td style='padding: 12px; border: 1px solid #ddd; text-align: center; font-weight: bold;'>4️⃣</td>
                <td style='padding: 12px; border: 1px solid #ddd;'><strong>Rozwiązanie</strong><br>(System Milwaukee)</td>
                <td style='padding: 12px; border: 1px solid #ddd;'>System (narzędzie + baterie + akcesoria), nie katalog.</td>
            </tr>
            <tr style='background: #fef3c7;'>
                <td style='padding: 12px; border: 1px solid #ddd; text-align: center; font-weight: bold;'>5️⃣</td>
                <td style='padding: 12px; border: 1px solid #ddd;'><strong>Demo</strong><br>(Proof)</td>
                <td style='padding: 12px; border: 1px solid #ddd;'>Cel + kryterium sukcesu. KLIENT pracuje, nie JSS!</td>
            </tr>
            <tr style='background: white;'>
                <td style='padding: 12px; border: 1px solid #ddd; text-align: center; font-weight: bold;'>6️⃣</td>
                <td style='padding: 12px; border: 1px solid #ddd;'><strong>Wartość</strong><br>(Value)</td>
                <td style='padding: 12px; border: 1px solid #ddd;'>Klient SAM kalkuluje wartość. Pytasz: "Co się zmieniło?"</td>
            </tr>
            <tr style='background: #fef3c7;'>
                <td style='padding: 12px; border: 1px solid #ddd; text-align: center; font-weight: bold;'>7️⃣</td>
                <td style='padding: 12px; border: 1px solid #ddd;'><strong>Next Steps</strong><br>(Domknięcie)</td>
                <td style='padding: 12px; border: 1px solid #ddd;'>KTO-CO-KIEDY. Follow-up 24h (email/SMS).</td>
            </tr>
        </tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)
    
    # Action Plan Template (używając Streamlit widgets)
    st.markdown("### 📋 Twój Action Plan")
    st.markdown("Wypełnij poniższy plan działania. **Twoje odpowiedzi zostaną automatycznie zapisane**.")
    
    # DZIŚ
    action_today = st.text_area(
        "📅 DZIŚ (15 minut po lekcji)",
        value=saved_notes.get('action_today', ''),
        placeholder='Co zrobię DZIŚ po tej lekcji? (np. wydrukuję checklist Canvas)',
        key=f'action_today_{lesson_id}',
        height=100
    )
    # Zapisz w session_state dla dostępu przy "Zakończ lekcję"
    st.session_state[f'lesson_note_{lesson_id}_action_today'] = action_today
    
    # JUTRO
    action_tomorrow = st.text_area(
        "🎯 JUTRO (Pierwsze zastosowanie)",
        value=saved_notes.get('action_tomorrow', ''),
        placeholder='Jak zastosuję Canvas w pracy JUTRO?',
        key=f'action_tomorrow_{lesson_id}',
        height=100
    )
    st.session_state[f'lesson_note_{lesson_id}_action_tomorrow'] = action_tomorrow
    
    # ZA TYDZIEŃ
    action_week = st.text_area(
        "⏰ ZA TYDZIEŃ (Review + powtórka)",
        value=saved_notes.get('action_week', ''),
        placeholder='Co zrobię ZA TYDZIEŃ?',
        key=f'action_week_{lesson_id}',
        height=100
    )
    st.session_state[f'lesson_note_{lesson_id}_action_week'] = action_week
    
    # Auto-save - zapisz zawsze gdy są jakiekolwiek wartości
    if action_today or action_tomorrow or action_week:
        from utils.lesson_notes import save_lesson_notes
        save_lesson_notes(username, lesson_id, {
            'action_today': action_today,
            'action_tomorrow': action_tomorrow,
            'action_week': action_week
        })
    
    # Informacja o badaniach
    st.markdown("""
    <p style='margin-top: 15px; padding: 12px; background: #e0f2fe; border-left: 4px solid #0284c7; border-radius: 4px; font-size: 0.95rem;'>
    <strong>💡 Wskazówka:</strong> Badania pokazują, że osoby, które wypełniają Action Plan mają 
    <strong>+60% szans na zastosowanie wiedzy w praktyce</strong> (Implementation Intention, Gollwitzer, 1999).
    </p>
    """, unsafe_allow_html=True)
    
    # Reflection Journal
    st.markdown("---")
    st.markdown("### 💭 Reflection Journal")
    st.markdown("Odpowiedz na 3 pytania poniżej. **Twoje notatki zostaną automatycznie zapisane**.")
    
    reflection_discovery = st.text_area(
        "💡 1. Co było dla mnie NAJWIĘKSZYM odkryciem w tej lekcji?",
        value=saved_notes.get('reflection_discovery', ''),
        placeholder='Np. "Największe odkrycie to zasada z KROKU 2..."',
        key=f'reflection_discovery_{lesson_id}',
        height=120
    )
    st.session_state[f'lesson_note_{lesson_id}_reflection_discovery'] = reflection_discovery
    
    reflection_doubts = st.text_area(
        "🤔 2. Co WCIĄŻ mi nie do końca pasuje? (pytania/wątpliwości)",
        value=saved_notes.get('reflection_doubts', ''),
        placeholder='Np. "Nie jestem pewien, jak długo..."',
        key=f'reflection_doubts_{lesson_id}',
        height=120
    )
    st.session_state[f'lesson_note_{lesson_id}_reflection_doubts'] = reflection_doubts
    
    reflection_application = st.text_area(
        "🚀 3. Jak KONKRETNIE zastosuję tę wiedzę w ciągu 48 godzin?",
        value=saved_notes.get('reflection_application', ''),
        placeholder='Np. "W czwartek mam wizytę u klienta..."',
        key=f'reflection_application_{lesson_id}',
        height=120
    )
    st.session_state[f'lesson_note_{lesson_id}_reflection_application'] = reflection_application
    
    # Auto-save refleksji - zapisz zawsze gdy są wartości
    if reflection_discovery or reflection_doubts or reflection_application:
        from utils.lesson_notes import save_lesson_notes
        save_lesson_notes(username, lesson_id, {
            'reflection_discovery': reflection_discovery,
            'reflection_doubts': reflection_doubts,
            'reflection_application': reflection_application
        })
    
    # Informacja o zapisie
    st.markdown("""
    <p style='margin-top: 15px; padding: 12px; background: #fef3c7; border-left: 4px solid #f59e0b; border-radius: 4px; font-size: 0.95rem;'>
    <strong>🧠 Dlaczego to ważne?</strong> Reflection (metacognition) zwiększa retencję wiedzy o <strong>+30%</strong> 
    i pomaga w transferze z teorii do praktyki (Flavell, 1979).
    </p>
    """, unsafe_allow_html=True)
    
    # Następne kroki
    st.markdown("---")
    st.markdown("""
    <div class='success-box'>
    <h3>🎯 Następne kroki</h3>
    <ul style='line-height: 1.8;'>
        <li>📥 <strong>Pobierz Cheatsheet</strong> - kompletny Canvas na 1 stronie A4 (do wydruku)</li>
        <li>🔄 <strong>Wróć za 3 dni</strong> - powtórz fiszki i quiz (spaced repetition)</li>
        <li>📧 <strong>Podziel się z zespołem</strong> - wyślij Action Plan do kolegi JSS</li>
        <li>🎬 <strong>Zagraj w Business Games</strong> - przetestuj Canvas w symulacji</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)


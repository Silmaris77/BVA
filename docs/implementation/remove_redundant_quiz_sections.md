# Usunięcie nadmiarowych sekcji w wynikach quizów autodiagnozy

## Problem
W wynikach quizów autodiagnozy wyświetlały się nadmiarowe sekcje:
- "📊 Szczegółowe wyniki quizu" (nagłówek)
- "🔍 Suma punktów autodiagnozy: X punktów" (blok z punktacją)

Te sekcje były redundantne, ponieważ:
1. Spersonalizowane wyniki już pokazują punktację w lepszym kontekście
2. Nagłówek "Szczegółowe wyniki" był niepotrzebny

## Rozwiązanie

### Usunięte elementy:
1. **Nagłówek sekcji** (linia ~3406)
   ```python
   st.markdown("---")
   st.markdown("## 📊 Szczegółowe wyniki quizu")
   ```

2. **Blok z sumą punktów** (linie ~3452-3465)
   ```python
   st.markdown(f"""
   <div style='background: linear-gradient(135deg, #9C27B020 0%, #9C27B010 100%); 
               padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 5px solid #9C27B0;'>
       <h3 style='color: #9C27B0; margin: 0;'>🔍 Suma punktów autodiagnozy</h3>
       <p style='font-size: 1.2rem; margin: 10px 0; color: #333;'>
           <strong>{total_points} punktów</strong>
       </p>
   </div>
   """, unsafe_allow_html=True)
   ```

### Zachowane elementy:
- **🔍 Twoje odpowiedzi** - sekcja z expanderem pokazującym szczegóły odpowiedzi
- Wszystkie funkcjonalności dla standardowych quizów testowych (bez zmian)

## Rezultat

### Nowa struktura quizów autodiagnozy:
1. ✅ Ukończyłeś już ten quiz w dniu: [data]
2. ✅ Dziękujemy za szczerą samorefleksję!
3. 🔍 Zobacz swoje poprzednie odpowiedzi:
   - **🎯 Twoje spersonalizowane wyniki** *(z właściwą punktacją i interpretacją)*
   - **🔍 Twoje odpowiedzi** *(expander z detalami - bez nadmiarowego nagłówka)*
4. 🔄 Przystąp do quizu ponownie

## Korzyści
- **Czytelniejszy interfejs** - mniej redundantnych informacji
- **Lepszy flow** - użytkownik przechodzi od spersonalizowanych wyników do detali
- **Spójność** - punkty są pokazane w kontekście interpretacji, nie jako surowa liczba

## Dotyczy
- Funkcja `display_quiz_results()` w `views/lesson.py`
- Tylko quizy autodiagnozy (`is_self_diagnostic = True`)
- Standardowe quizy testowe pozostają bez zmian

## Data: 2024-12-22
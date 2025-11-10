"""
FMCG Conviction AI Evaluator
Ocenia argumenty sprzedażowe gracza używając Gemini 2.5 Flash
System 3-etapowy: Discovery → Pitch → Convince
"""

import google.generativeai as genai
from typing import Dict, Tuple, Optional
from datetime import datetime
import streamlit as st


def get_gemini_api_key() -> Optional[str]:
    """Pobiera klucz API Gemini z secrets lub environment"""
    try:
        if hasattr(st, 'secrets') and 'API_KEYS' in st.secrets:
            if 'GEMINI_API_KEY' in st.secrets['API_KEYS']:
                return st.secrets['API_KEYS']['GEMINI_API_KEY']
            elif 'gemini' in st.secrets['API_KEYS']:
                return st.secrets['API_KEYS']['gemini']
    except:
        pass
    
    import os
    return os.getenv('GEMINI_API_KEY')


def evaluate_sales_argument(
    client_data: Dict,
    product_id: str,
    argument_text: str,
    current_stage: str,
    current_progress: int,
    conversation_history: list = None
) -> Tuple[int, str, bool, str]:
    """
    Ocenia argument sprzedażowy gracza używając Gemini AI
    
    Args:
        client_data: Dane klienta (name, type, segment, current_competitors, etc.)
        product_id: ID produktu Heinz (np. 'heinz_ketchup_premium_5kg')
        argument_text: Argument gracza do oceny
        current_stage: Aktualny etap (discovery, pitch, convince)
        current_progress: Aktualny progress 0-100
        conversation_history: Historia poprzednich argumentów
    
    Returns:
        Tuple (score, feedback, stage_complete, next_stage)
        - score: 0-100 (jakość argumentu)
        - feedback: AI feedback dla gracza
        - stage_complete: czy etap zakończony (True = można przejść dalej)
        - next_stage: następny etap ('discovery', 'pitch', 'convince', 'won')
    """
    
    # Inicjalizuj Gemini
    api_key = get_gemini_api_key()
    if not api_key:
        return 50, "⚠️ Brak klucza API Gemini - argument zapisany bez oceny.", False, current_stage
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemini-2.0-flash-exp")
        
        # Przygotuj informacje o produkcie
        product_info = get_product_info(product_id)
        
        # Przygotuj informacje o kliencie
        client_name = client_data.get('name', 'Klient')
        client_type = client_data.get('type', 'Restauracja')
        client_segment = client_data.get('segment', 'mixed')
        current_competitors = client_data.get('current_competitors', {})
        monthly_covers = client_data.get('monthly_covers', 0)
        
        # Historia poprzednich argumentów (ostatnie 3)
        history_context = ""
        if conversation_history:
            recent_history = conversation_history[-3:]
            history_context = "\n\n**HISTORIA POPRZEDNICH ARGUMENTÓW:**\n"
            for i, conv in enumerate(recent_history, 1):
                arg = conv.get('player_argument', '')
                score = conv.get('ai_score', 0)
                feedback = conv.get('ai_feedback', '')
                history_context += f"\nArgument {i} (ocena: {score}/100):\n{arg}\nFeedback: {feedback}\n"
        
        # Określ cel etapu
        stage_goals = {
            'discovery': """
**CEL ETAPU DISCOVERY (0-33%):**
- Zrozumieć potrzeby i sytuację klienta
- Przedstawić główne korzyści produktu Heinz
- Zbudować zainteresowanie i zaufanie
- Pokazać znajomość branży i produktu
- NIEDOPUSZCZALNE: podawanie ceny, konkretnej oferty (to etap Pitch)
            """,
            'pitch': """
**CEL ETAPU PITCH (34-66%):**
- Przedstawić konkretną ofertę cenową
- Wskazać dystrybutora i warunki dostawy
- Pokazać ROI i oszczędności (jeśli zastąpienie konkurencji)
- Zaproponować próbkę lub test produktu
- NIEDOPUSZCZALNE: tylko ogólniki bez konkretów cenowych
            """,
            'convince': """
**CEL ETAPU CONVINCE (67-100%):**
- Odpowiedzieć na ostatnie obiekcje klienta
- Uzyskać commitment do zakupu
- Potwierdzić szczegóły zamówienia
- Zamknąć sprzedaż (close the deal)
- NIEDOPUSZCZALNE: cofanie się do Discovery lub Pitch - to finalizacja
            """
        }
        
        current_goal = stage_goals.get(current_stage, stage_goals['discovery'])
        
        # Prompt dla Gemini
        prompt = f"""Jesteś ekspertem od sprzedaży B2B w branży FMCG (Food Service). Oceniasz argument sprzedażowy gracza.

**KONTEKST KLIENTA:**
- Nazwa: {client_name}
- Typ: {client_type}
- Segment: {client_segment}
- Miesięczne pokrycia: {monthly_covers}
- Obecna konkurencja: {current_competitors}

**PRODUKT HEINZ:**
{product_info}

**AKTUALNY ETAP CONVICTION:**
Etap: **{current_stage.upper()}** (Progress: {current_progress}%)
{current_goal}
{history_context}

**ARGUMENT GRACZA DO OCENY:**
"{argument_text}"

---

**ZADANIE:**
Oceń powyższy argument gracza w skali 0-100 biorąc pod uwagę:

1. **Relevance (30 pkt):** Czy argument pasuje do potrzeb tego konkretnego klienta i etapu?
2. **Persuasiveness (30 pkt):** Czy argument jest przekonujący i konkretny?
3. **Product Knowledge (20 pkt):** Czy gracz pokazuje znajomość produktu Heinz?
4. **Stage Appropriateness (20 pkt):** Czy argument jest odpowiedni dla etapu {current_stage}?

**SCORING:**
- 90-100: Perfekcyjny argument - etap zakończony, przejście do następnego
- 80-89: Świetny argument - duży postęp (+30-40%)
- 70-79: Dobry argument - średni postęp (+20-30%)
- 60-69: Okej argument - mały postęp (+10-20%)
- 50-59: Słaby argument - minimalny postęp (+5-10%)
- 0-49: Bardzo słaby - brak postępu lub regres

**WAŻNE ZASADY:**
- Etap Discovery kończy się przy ≥33% (przejście do Pitch)
- Etap Pitch kończy się przy ≥66% (przejście do Convince)
- Etap Convince kończy się przy ≥100% (WON - klient przekonany!)
- Jeśli gracz używa argumentów z INNEGO etapu (np. ceny w Discovery) - niższa ocena
- Jeśli gracz powtarza argumenty z historii - niższa ocena

**FORMAT ODPOWIEDZI (OBOWIĄZKOWY JSON):**
```json
{{
  "score": <0-100>,
  "feedback": "<konkretny feedback dla gracza - co zrobił dobrze, co poprawić, następny krok>",
  "progress_gain": <ile % dodać do progress, na podstawie score>,
  "stage_complete": <true/false - czy można przejść do następnego etapu>,
  "next_stage": "<discovery/pitch/convince/won>"
}}
```

Odpowiedz TYLKO JSON, bez dodatkowych komentarzy."""

        # Wywołaj Gemini
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Parse JSON z odpowiedzi
        import json
        import re
        
        # Usuń markdown code blocks jeśli istnieją
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(1)
        
        # Parse JSON
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback - spróbuj wyciągnąć JSON z tekstu
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(0))
            else:
                # Ostateczny fallback
                return 60, "✅ Argument zapisany. (AI nie mogło wygenerować oceny - spróbuj ponownie)", False, current_stage
        
        # Wyciągnij wartości
        score = int(result.get('score', 60))
        feedback = result.get('feedback', 'Argument zapisany.')
        progress_gain = int(result.get('progress_gain', 10))
        stage_complete = result.get('stage_complete', False)
        next_stage = result.get('next_stage', current_stage)
        
        # Walidacja wartości
        score = max(0, min(100, score))
        progress_gain = max(0, min(50, progress_gain))  # Max +50% na raz
        
        # Logika zmiany etapu
        new_progress = min(100, current_progress + progress_gain)
        
        if current_stage == 'discovery' and new_progress >= 34:
            next_stage = 'pitch'
            stage_complete = True
        elif current_stage == 'pitch' and new_progress >= 67:
            next_stage = 'convince'
            stage_complete = True
        elif current_stage == 'convince' and new_progress >= 100:
            next_stage = 'won'
            stage_complete = True
        else:
            next_stage = current_stage
            stage_complete = False
        
        return score, feedback, stage_complete, next_stage
        
    except Exception as e:
        error_msg = f"⚠️ Błąd AI evaluation: {str(e)[:100]}"
        return 50, error_msg, False, current_stage


def get_product_info(product_id: str) -> str:
    """Zwraca informacje o produkcie Heinz"""
    
    products = {
        'heinz_ketchup_premium_5kg': """
**Heinz Ketchup Premium 5kg**
- Brix: 29% (najgęstszy na rynku - oznacza mniej zużycia)
- Składniki: 148g pomidorów na 100g produktu
- Konsystencja: Gęsta, nie rozwarstwiająca się
- Premium brand: Rozpoznawalność międzynarodowa
- Cena hurtowa: ~38-42 PLN/5kg (zależnie od dystrybutora)
- Konkurencja: Pudliszki (28 PLN), Kotlin (32 PLN), Develey (35 PLN)
- ROI: 15% mniejsze zużycie = oszczędność przy dużych wolumenach
        """,
        'heinz_majonez_delikatny_5kg': """
**Heinz Majonez Delikatny 5kg**
- Zawartość oleju: 78% (więcej niż konkurencja)
- Konsystencja: Stabilna w różnych temperaturach
- Smak: Delikatny, uniwersalny (sałatki, sosy, burgery)
- Premium brand: Heinz = jakość w oczach gości
- Cena hurtowa: ~40-44 PLN/5kg
- Konkurencja: Winiary (30 PLN), Kotlin (35 PLN), Hellmann's (45 PLN)
- USP: Stabilność smaku niezależnie od aplikacji
        """,
        'heinz_majonez_premium_5l': """
**Heinz Majonez Premium 5L**
- Zawartość oleju: 80% (premium line)
- Pojemność: 5L (większe opakowanie dla dużych kuchni)
- Zastosowanie: Hotele, catering, duże restauracje
- Konsystencja: Bardzo stabilna, nie rozdziela się
- Cena hurtowa: ~55-60 PLN/5L
- Konkurencja: Hellmann's Professional (58 PLN), Develey (52 PLN)
        """,
        'heinz_bbq_sauce_original_2_5kg': """
**Heinz BBQ Sauce Original 2.5kg**
- Styl: American-style BBQ (słodko-wędzony)
- Pomidory: 35% (więcej niż konkurencja)
- Konsystencja: Gęsta, idealnie przywiera do mięsa
- Zastosowanie: Żeberka, burgery, pulled pork, grillowane kurczaki
- Cena hurtowa: ~42-46 PLN/2.5kg
- Konkurencja: Develey BBQ (38 PLN), Jack Daniel's (60 PLN premium)
- USP: Gęstość = mniej zużycia na porcję
        """,
        'heinz_bbq_premium_3l': """
**Heinz BBQ Premium 3L**
- Premium line: Intensywniejszy smak
- Pojemność: 3L (dla grill houses i smokehouse)
- Inspiracja: Texas BBQ
- Zastosowanie: Profesjonalne grille, BBQ restaurants
- Cena hurtowa: ~58-62 PLN/3L
- Konkurencja: Jack Daniel's (65 PLN), własne mieszanki (różnie)
        """,
        'heinz_sticky_korean_sauce_2_35kg': """
**Heinz Sticky Korean Sauce 2.35kg**
- Trend: Korean fusion (gochujang-style)
- Profil: Słodko-pikantny, lepki (sticky)
- Zastosowanie: Korean fried chicken, burgery fusion, wrap'y
- Target: Premium restaurants, hotele, fusion cuisine
- Cena hurtowa: ~48-52 PLN/2.35kg
- Konkurencja: Brak bezpośredniej (niszowy produkt)
- USP: Gotowy sos trendy bez mieszania składników
        """,
        'heinz_mayonnaise_professional_10l': """
**Heinz Mayonnaise Professional 10L**
- Linia: Professional (dla QSR i chains)
- Pojemność: 10L (największe opakowanie)
- Target: McDonald's, KFC, duże sieci
- Zawartość oleju: 78%
- Cena hurtowa: ~95-105 PLN/10L
- Konkurencja: Hellmann's Professional (100 PLN)
- USP: Konsystencja idealna dla dozowników automatycznych
        """
    }
    
    return products.get(product_id, f"**{product_id}** - Produkt Heinz Food Service")

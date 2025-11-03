"""
FMCG AI Conversation Engine
Obsługuje rozmowy AI z klientami FMCG używając Gemini 2.0 Flash
"""

import google.generativeai as genai
import os
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import streamlit as st

from data.industries.fmcg_conversations import build_conversation_prompt


def get_gemini_api_key() -> Optional[str]:
    """Pobiera klucz API Gemini z secrets lub environment"""
    # Try Streamlit secrets first
    try:
        if hasattr(st, 'secrets') and 'API_KEYS' in st.secrets:
            if 'GEMINI_API_KEY' in st.secrets['API_KEYS']:
                return st.secrets['API_KEYS']['GEMINI_API_KEY']
    except:
        pass
    
    # Try config file
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(current_dir)
        api_key_file = os.path.join(base_dir, "config", "gemini_api_key.txt")
        
        if os.path.exists(api_key_file):
            with open(api_key_file, 'r') as f:
                key = f.read().strip()
                if key:
                    return key
    except:
        pass
    
    # Try environment variable
    return os.getenv('GEMINI_API_KEY')


def initialize_gemini() -> bool:
    """
    Inicjalizuje Gemini API
    
    Returns:
        True jeśli sukces
    """
    api_key = get_gemini_api_key()
    
    if not api_key:
        return False
    
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"❌ Błąd inicjalizacji Gemini: {e}")
        return False


def conduct_fmcg_conversation(
    client: Dict,
    player_message: str,
    conversation_history: List[Dict] = None,
    current_messages: List[Dict] = None
) -> Tuple[str, Dict]:
    """
    Prowadzi rozmowę AI z klientem FMCG
    
    Args:
        client: FMCGClientData - dane klienta
        player_message: Wiadomość od gracza
        conversation_history: Historia poprzednich wizyt
        current_messages: Historia wiadomości z bieżącej rozmowy
    
    Returns:
        Tuple (AI response text, metadata)
    """
    # Initialize Gemini
    if not initialize_gemini():
        return "Przepraszam, system AI jest obecnie niedostępny.", {"error": "no_api_key"}
    
    # Build context
    context = {
        "relationship_status": client.get("status", "PROSPECT"),
        "products_sold": [],
        "relationship_score": client.get("reputation", 0) if client.get("status") == "ACTIVE" else 0
    }
    
    # Build prompt
    prompt = build_conversation_prompt(
        customer=client,
        conversation_history=conversation_history or [],
        player_message=player_message,
        context=context,
        current_messages=current_messages or []
    )
    
    try:
        # Use Gemini 2.0 Flash
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Generate response
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.9,  # More creative/natural
                top_p=0.95,
                top_k=40,
                max_output_tokens=500,  # Reasonable conversation length
            )
        )
        
        # Safely extract text from response
        try:
            ai_response = response.text
        except (AttributeError, ValueError, KeyError) as e:
            # Response might be blocked or empty
            print(f"⚠️ Błąd odczytu response.text: {e}")
            print(f"Response type: {type(response)}")
            if hasattr(response, 'candidates') and response.candidates:
                try:
                    if response.candidates[0].content.parts:
                        part = response.candidates[0].content.parts[0]
                        # Try different ways to get text
                        if hasattr(part, 'text'):
                            ai_response = part.text
                        elif isinstance(part, dict) and 'text' in part:
                            ai_response = part['text']
                        else:
                            ai_response = "Przepraszam, nie mogę w tym momencie odpowiedzieć."
                    else:
                        ai_response = "Przepraszam, nie mogę w tym momencie odpowiedzieć."
                except (AttributeError, KeyError, IndexError) as part_error:
                    print(f"⚠️ Błąd odczytu parts: {part_error}")
                    ai_response = "Przepraszam, wystąpił problem z odpowiedzią."
            else:
                ai_response = "Przepraszam, wystąpił problem z odpowiedzią."
        
        # Metadata
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "model": "gemini-2.0-flash-exp",
            "success": True
        }
        
        return ai_response, metadata
        
    except Exception as e:
        print(f"❌ Błąd Gemini API: {e}")
        return f"Przepraszam, mam chwilowy problem z odpowiedzią. (Błąd: {str(e)})", {"error": str(e)}


def evaluate_conversation_quality(
    conversation_messages: List[Dict],
    client: Dict
) -> Dict:
    """
    Ocenia jakość rozmowy gracza używając AI
    
    Args:
        conversation_messages: Lista wiadomości z rozmowy
        client: Dane klienta
    
    Returns:
        Dict z oceną (quality 1-5, order_likely, reputation_change)
    """
    # Initialize Gemini
    if not initialize_gemini():
        return {
            "quality": 3,
            "order_likely": False,
            "order_value": 0,
            "reputation_change": 0,
            "feedback": "System oceny niedostępny"
        }
    
    # Build evaluation prompt
    conversation_text = "\n\n".join([
        f"{'Handlowiec' if msg['role'] == 'player' else 'Klient'}: {msg['content']}"
        for msg in conversation_messages
    ])
    
    client_name = client.get("name", "klient")
    client_type = client.get("type", "sklep")
    client_personality = client.get("owner_profile", {}).get("personality", {})
    
    evaluation_prompt = f"""
Jesteś ekspertem od sprzedaży FMCG. Oceń jakość rozmowy handlowej.

KLIENT: {client_name} ({client_type})
OSOBOWOŚĆ właściciela: {client_personality}

ROZMOWA:
{conversation_text}

OCEŃ (odpowiedz TYLKO w formacie JSON):
{{
    "quality": 1-5,  // 1=fatalna, 2=słaba, 3=OK, 4=dobra, 5=świetna
    "order_likely": true/false,  // Czy klient złoży zamówienie?
    "order_value": 0-5000,  // Szacowana wartość zamówienia PLN
    "reputation_change": -20 do +20,  // Zmiana reputacji
    "feedback": "Krótkie uzasadnienie (2-3 zdania)"
}}

KRYTERIA OCENY:
- Czy handlowiec słuchał klienta?
- Czy dostosował ofertę do potrzeb?
- Czy był profesjonalny i uprzejmy?
- Czy zbudował zaufanie?
- Czy przedstawił wartość produktów?
- Czy zamknął sprzedaż skutecznie?

Odpowiedz TYLKO JSON (bez markdown, bez dodatkowego tekstu):
"""
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        response = model.generate_content(
            evaluation_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,  # Lower temperature for more consistent evaluation
                top_p=0.9,
                max_output_tokens=300,
            )
        )
        
        # Parse JSON response
        import json
        import re
        
        # Get response text safely
        try:
            response_text = response.text.strip()
        except AttributeError:
            # If response doesn't have .text attribute, fallback
            print(f"❌ Błąd: response nie ma atrybutu 'text'")
            return evaluate_conversation_heuristic(conversation_messages, client)
        
        # Remove markdown code blocks if present
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*$', '', response_text)
        response_text = response_text.strip()
        
        try:
            evaluation = json.loads(response_text)
        except json.JSONDecodeError as json_err:
            print(f"❌ Błąd parsowania JSON: {json_err}")
            print(f"Response text: {response_text[:200]}...")
            return evaluate_conversation_heuristic(conversation_messages, client)
        
        # Validate and cap values
        evaluation["quality"] = max(1, min(5, int(evaluation.get("quality", 3))))
        evaluation["order_likely"] = bool(evaluation.get("order_likely", False))
        evaluation["order_value"] = max(0, min(5000, int(evaluation.get("order_value", 0))))
        evaluation["reputation_change"] = max(-20, min(20, int(evaluation.get("reputation_change", 0))))
        evaluation["feedback"] = str(evaluation.get("feedback", "Brak oceny"))
        
        return evaluation
        
    except Exception as e:
        print(f"❌ Błąd oceny rozmowy: {e}")
        print(f"Exception type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        # Fallback to simple heuristic
        return evaluate_conversation_heuristic(conversation_messages, client)


def evaluate_conversation_heuristic(
    conversation_messages: List[Dict],
    client: Dict
) -> Dict:
    """
    Prosta heurystyczna ocena rozmowy (fallback gdy AI niedostępne)
    
    Args:
        conversation_messages: Lista wiadomości
        client: Dane klienta
    
    Returns:
        Dict z oceną
    """
    # Count messages
    player_messages = [msg for msg in conversation_messages if msg['role'] == 'player']
    ai_messages = [msg for msg in conversation_messages if msg['role'] == 'assistant']
    
    # Simple scoring
    quality = 3  # Default OK
    
    # Bonus for engagement
    if len(player_messages) >= 3:
        quality += 1
    
    # Bonus for longer messages (shows effort)
    avg_length = sum(len(msg['content']) for msg in player_messages) / max(1, len(player_messages))
    if avg_length > 100:
        quality += 1
    
    # Cap at 5
    quality = min(5, quality)
    
    # Estimate order likelihood
    order_likely = quality >= 4
    order_value = 2000 if order_likely else 0
    
    # Reputation change
    reputation_change = (quality - 3) * 5  # -10 to +10
    
    return {
        "quality": quality,
        "order_likely": order_likely,
        "order_value": order_value,
        "reputation_change": reputation_change,
        "feedback": f"Rozmowa oceniona na {quality}/5 gwiazdek (ocena automatyczna)"
    }


def generate_conversation_summary(
    conversation_messages: List[Dict],
    client: Dict,
    evaluation: Dict
) -> Dict:
    """
    Generuje podsumowanie rozmowy dla historii
    
    Args:
        conversation_messages: Lista wiadomości z rozmowy
        client: Dane klienta
        evaluation: Wynik ewaluacji rozmowy
    
    Returns:
        Dict z podsumowaniem {summary: str, key_points: List[str]}
    """
    if not initialize_gemini():
        # Fallback - proste podsumowanie
        return {
            "summary": f"Wizyta u {client.get('name', 'klienta')}. Rozmowa na {evaluation['quality']}/5.",
            "key_points": [
                f"Jakość rozmowy: {evaluation['quality']}/5",
                f"Zamówienie: {'TAK' if evaluation['order_likely'] else 'NIE'}",
                f"Wartość: {evaluation['order_value']} PLN"
            ]
        }
    
    # Build summary prompt
    conversation_text = "\n".join([
        f"{'Handlowiec' if msg['role'] == 'player' else 'Klient'}: {msg['content']}"
        for msg in conversation_messages
    ])
    
    client_name = client.get("name", "klient")
    
    summary_prompt = f"""
Jesteś asystentem handlowca FMCG. Wygeneruj KRÓTKIE podsumowanie wizyty.

ROZMOWA z {client_name}:
{conversation_text}

WYNIK:
- Jakość: {evaluation['quality']}/5
- Zamówienie: {'TAK ({} PLN)'.format(evaluation['order_value']) if evaluation['order_likely'] else 'NIE'}
- Reputacja: {evaluation['reputation_change']:+d}

Wygeneruj JSON:
{{
    "summary": "1-2 zdania podsumowania (CO się stało, JAK poszło)",
    "key_points": ["Punkt 1: kluczowe ustalenie", "Punkt 2: obietnica/zobowiązanie", "Punkt 3: następne kroki"]
}}

WAŻNE:
- summary: max 2 zdania, konkretnie
- key_points: 2-4 punkty, tylko NAJWAŻNIEJSZE ustalenia/obietnice
- Jeśli handlowiec coś obiecał → KONIECZNIE w key_points
- Jeśli klient coś uzależnił (np. "zadzwoń za tydzień") → w key_points

Odpowiedz TYLKO JSON:
"""
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(summary_prompt)
        
        # Parse JSON
        import json
        import re
        
        # Safely extract text from response
        try:
            response_text = response.text.strip()
        except (AttributeError, ValueError) as e:
            print(f"⚠️ Błąd odczytu response.text w generate_conversation_summary: {e}")
            # Fallback - simple summary
            return {
                "summary": f"Wizyta u {client_name}. Rozmowa na {evaluation['quality']}/5.",
                "key_points": [
                    f"Jakość: {evaluation['quality']}/5",
                    f"Zamówienie: {'TAK' if evaluation['order_likely'] else 'NIE'} ({evaluation['order_value']} PLN)"
                ]
            }
        
        # Remove markdown if present
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*$', '', response_text)
        
        result = json.loads(response_text)
        
        return {
            "summary": result.get("summary", "Wizyta zakończona"),
            "key_points": result.get("key_points", [])
        }
        
    except Exception as e:
        print(f"❌ Błąd generowania podsumowania: {e}")
        # Fallback
        return {
            "summary": f"Wizyta u {client_name}. Rozmowa na {evaluation['quality']}/5.",
            "key_points": [
                f"Jakość: {evaluation['quality']}/5",
                f"Zamówienie: {'TAK' if evaluation['order_likely'] else 'NIE'} ({evaluation['order_value']} PLN)"
            ]
        }


def generate_manager_feedback_fuko(
    conversation_messages: List[Dict],
    client: Dict,
    evaluation: Dict
) -> List[Dict]:
    """
    Generuje feedback menedżerski w formule FUKO
    
    Args:
        conversation_messages: Lista wiadomości z rozmowy
        client: Dane klienta
        evaluation: Ocena rozmowy
    
    Returns:
        Lista 2 obszarów feedbacku w formule FUKO
    """
    # Initialize Gemini
    if not initialize_gemini():
        return [{
            "area": "Komunikacja",
            "fakty": "Przeprowadzona rozmowa z klientem.",
            "ustosunkowanie": "Rozmowa wymagała większego zaangażowania.",
            "konsekwencje": "Potencjalnie niższa wartość zamówienia.",
            "oczekiwania": "Zwiększ aktywność w zadawaniu pytań i budowaniu relacji."
        }]
    
    # Build conversation transcript
    transcript = ""
    for msg in conversation_messages:
        role_label = "Handlowiec" if msg['role'] == 'player' else f"{client.get('owner', 'Klient')}"
        transcript += f"{role_label}: {msg['content']}\n\n"
    
    client_name = client.get('name', 'klient')
    
    fuko_prompt = f"""
Jesteś doświadczonym menedżerem sprzedaży FMCG. Obserwowałeś wizytę handlową Twojego podwładnego u klienta {client_name}.

TRANSKRYPT ROZMOWY:
{transcript}

OCENA WIZYTY:
- Jakość rozmowy: {evaluation['quality']}/5
- Zamówienie prawdopodobne: {'TAK' if evaluation['order_likely'] else 'NIE'}
- Wartość zamówienia: {evaluation['order_value']} PLN
- Zmiana reputacji: {evaluation.get('reputation_change', 0)}

TWOJE ZADANIE:
Przygotuj feedback rozwojowy dla handlowca dotyczący 2 najważniejszych obszarów do poprawy.
WAŻNE: Zwracaj się bezpośrednio do handlowca w drugiej osobie ("Ty", "zapytałeś", "powiedziałeś", "zrobiłeś" itp.)

OBSZARY DO ANALIZY:
1. Nawiązanie kontaktu i budowanie relacji
2. Identyfikacja potrzeb klienta (pytania odkrywające)
3. Prezentacja wartości produktu/rozwiązania
4. Obsługa obiekcji
5. Zamykanie sprzedaży (closing)
6. Budowanie długoterminowej współpracy

STRUKTURA FEEDBACKU (FUKO):
- **Fakty** - konkretne zachowania zaobserwowane w rozmowie (cytuj fragmenty), używaj zwrotów typu "zapytałeś", "powiedziałeś", "zacząłeś od"
- **Ustosunkowanie** - Twoja ocena tych zachowań (co było dobre, co wymaga poprawy), używaj zwrotów typu "doceniam że...", "zauważyłem że..."
- **Konsekwencje** - jakie skutki mają/będą miały te zachowania, używaj zwrotów typu "dzięki temu...", "przez to..."
- **Oczekiwania** - konkretne zachowania/techniki, których oczekujesz w przyszłości, używaj zwrotów typu "oczekuję że...", "w następnej wizycie zapytaj o..."

ZASADY:
- Wybierz 2 NAJWAŻNIEJSZE obszary (nie wszystkie!)
- Bądź konkretny - odwołuj się do faktycznych fragmentów rozmowy
- Balans: konstruktywna krytyka + wskazówki rozwojowe
- Język profesjonalny ale przyjazny
- ZAWSZE używaj drugiej osoby ("Ty") - nigdy nie mów "handlowiec", "przedstawiciel" itp.
- Przykłady dobrych zwrotów: "Na początku rozmowy zapytałeś...", "Zauważyłem, że pominąłeś...", "W następnej wizycie spróbuj..."

Odpowiedz w formacie JSON:
{{
  "feedback": [
    {{
      "area": "Nazwa obszaru (np. 'Identyfikacja potrzeb')",
      "fakty": "Konkretny opis zaobserwowanych zachowań z przykładami z rozmowy (używaj 'zapytałeś', 'powiedziałeś' itp.)",
      "ustosunkowanie": "Twoja ocena - co było dobre/słabe (używaj 'doceniam że...', 'zauważyłem że...' itp.)",
      "konsekwencje": "Jakie skutki ma/będzie miało to zachowanie (używaj 'dzięki temu...', 'przez to...' itp.)",
      "oczekiwania": "Konkretne wskazówki co robić inaczej/lepiej (używaj 'oczekuję że...', 'spróbuj...' itp.)"
    }},
    {{
      "area": "Drugi obszar",
      "fakty": "...",
      "ustosunkowanie": "...",
      "konsekwencje": "...",
      "oczekiwania": "..."
    }}
  ]
}}
"""
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(
            fuko_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,  # Balanced - professional but not too rigid
                top_p=0.9,
                max_output_tokens=1500,
            )
        )
        
        # Parse JSON
        import json
        import re
        
        # Safely extract text from response
        try:
            response_text = response.text.strip()
        except (AttributeError, ValueError) as e:
            print(f"⚠️ Błąd odczytu response.text w generate_manager_feedback_fuko: {e}")
            # Return fallback feedback
            return [
                {
                    "area": "Komunikacja z klientem",
                    "fakty": "Podczas rozmowy zauważyłem Twoje zaangażowanie w prezentację produktów.",
                    "ustosunkowanie": "Pozytywnie oceniam Twoją energię, jednak rozmowa mogła być bardziej zorientowana na potrzeby klienta.",
                    "konsekwencje": "Klient może czuć się przytłoczony informacjami zamiast zrozumiany w swoich potrzebach.",
                    "oczekiwania": "W następnej wizycie zacznij od pytań odkrywających potrzeby klienta, zanim przejdziesz do prezentacji produktów."
                }
            ]
        
        # Remove markdown if present
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*$', '', response_text)
        
        result = json.loads(response_text)
        
        return result.get("feedback", [])
        
    except Exception as e:
        print(f"❌ Błąd generowania feedbacku FUKO: {e}")
        # Fallback
        return [
            {
                "area": "Komunikacja z klientem",
                "fakty": "Podczas rozmowy zauważyłem Twoje zaangażowanie w prezentację produktów.",
                "ustosunkowanie": "Pozytywnie oceniam Twoją energię, jednak rozmowa mogła być bardziej zorientowana na potrzeby klienta.",
                "konsekwencje": "Klient może czuć się przytłoczony informacjami zamiast zrozumiany w swoich potrzebach.",
                "oczekiwania": "W następnej wizycie zacznij od pytań odkrywających potrzeby klienta, zanim przejdziesz do prezentacji produktów."
            },
            {
                "area": "Zamykanie sprzedaży",
                "fakty": f"Rozmowa zakończyła się oceną {evaluation['quality']}/5, z szansą na zamówienie wartości {evaluation['order_value']} PLN.",
                "ustosunkowanie": "Widoczny postęp, ale brakuje wyraźnego call-to-action na koniec rozmowy.",
                "konsekwencje": "Bez jasnego następnego kroku klient może nie podjąć decyzji zakupowej.",
                "oczekiwania": "Zawsze kończ rozmowę konkretnym pytaniem zamykającym lub ustaleniem kolejnego kroku (np. 'Czy mogę przygotować zamówienie na...?')"
            }
        ]


def extract_client_discoveries(
    conversation_history: List[Dict],
    client_name: str,
    client_current_info: Dict
) -> Dict:
    """
    Wyciąga nowe informacje o kliencie z rozmowy używając Gemini AI
    
    Args:
        conversation_history: Lista wiadomości [{"role": "user"/"model", "text": "..."}]
        client_name: Nazwa klienta
        client_current_info: Obecne informacje o kliencie (FMCGClientDiscoveredInfo)
    
    Returns:
        Dict z odkrytymi informacjami (tylko te które są nowe lub zaktualizowane)
    """
    if not initialize_gemini():
        return {}
    
    # Build conversation transcript
    transcript = "\n".join([
        f"{'Handlowiec' if msg['role'] == 'user' else client_name}: {msg.get('content', msg.get('text', ''))}"
        for msg in conversation_history
    ])
    
    prompt = f"""Jesteś ekspertem sprzedaży B2B analizującym rozmowę handlową. Twoim zadaniem jest wyciągnąć nowe informacje o kliencie z transkryptu rozmowy.

TRANSKRYPT ROZMOWY:
{transcript}

OBECNE INFORMACJE O KLIENCIE:
{_format_current_info(client_current_info)}

INSTRUKCJA:
Przeanalizuj rozmowę i wyciągnij TYLKO te informacje, które:
1. Są bezpośrednio wspomniane przez klienta w rozmowie
2. Są nowe lub bardziej szczegółowe niż obecne informacje
3. Są faktami, nie założeniami

DOSTĘPNE KATEGORIE INFORMACJI:
- personality_description: Charakterystyka osobowości właściciela (jak podejmuje decyzje, na co zwraca uwagę)
- decision_priorities: Lista priorytetów przy podejmowaniu decyzji (np. ["Cena", "Jakość", "Wsparcie"])
- main_customers: Kim są główni klienci sklepu (demografia, wiek, potrzeby)
- customer_demographics: Szczegółowa demografia klientów
- competing_brands: Lista marek konkurencji które klient już sprzedaje
- shelf_space_constraints: Ograniczenia przestrzeni na półce
- pain_points: Lista problemów/bolączek klienta (co go frustruje, z czym się boryka)
- business_goals: Cele biznesowe klienta (co chce osiągnąć)
- typical_order_value: Typowa wartość zamówienia (zakres w PLN)
- preferred_frequency: Jak często preferuje zamawiać (np. "Co 2 tygodnie")
- payment_terms: Preferencje płatności
- delivery_preferences: Preferencje dotyczące dostaw
- best_selling_categories: Kategorie produktów które najlepiej się sprzedają
- seasonal_patterns: Wzorce sezonowe w sprzedaży
- trust_level: Poziom zaufania do handlowca (Sceptyczny/Otwarty/Zaufany partner)
- preferred_communication: Jak klient preferuje komunikację

WAŻNE:
- Jeśli informacja nie pojawia się w rozmowie, NIE dodawaj jej
- Cytuj fragment rozmowy jako kontekst dla każdego odkrycia
- Zwróć TYLKO nowe/zaktualizowane informacje

Odpowiedz w formacie JSON:
{{
    "discovered": {{
        "pole1": "wartość1",
        "pole2": ["wartość1", "wartość2"],
        ...
    }},
    "notes": [
        {{
            "field": "nazwa_pola",
            "value": "odkryta wartość",
            "context": "fragment rozmowy gdzie to zostało wspomniane"
        }}
    ]
}}
"""
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,  # Low - want factual extraction
                top_p=0.9,
                max_output_tokens=1000,
            )
        )
        
        # Parse JSON
        import json
        import re
        
        # Safely extract text from response
        try:
            response_text = response.text.strip()
        except (AttributeError, ValueError) as e:
            print(f"⚠️ Błąd odczytu response.text w extract_client_discoveries: {e}")
            return {"discovered": {}, "notes": []}
        
        # Remove markdown if present
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*$', '', response_text)
        
        result = json.loads(response_text)
        
        return result
        
    except Exception as e:
        print(f"❌ Błąd ekstrakcji informacji o kliencie: {e}")
        return {"discovered": {}, "notes": []}


def _format_current_info(current_info: Dict) -> str:
    """Formatuje obecne informacje o kliencie dla prompta"""
    lines = []
    for key, value in current_info.items():
        if value is None or value == "":
            lines.append(f"- {key}: DO USTALENIA")
        else:
            lines.append(f"- {key}: {value}")
    return "\n".join(lines) if lines else "Brak informacji (pierwsza wizyta)"


def calculate_knowledge_level(discovered_info: Dict) -> int:
    """
    Oblicza poziom znajomości klienta (0-5 stars) na podstawie % odkrytych pól
    
    Args:
        discovered_info: FMCGClientDiscoveredInfo dict
    
    Returns:
        0-5 (liczba gwiazdek)
    """
    # Wszystkie możliwe pola do odkrycia
    all_fields = [
        "personality_description",
        "decision_priorities",
        "main_customers",
        "customer_demographics",
        "competing_brands",
        "shelf_space_constraints",
        "pain_points",
        "business_goals",
        "typical_order_value",
        "preferred_frequency",
        "payment_terms",
        "delivery_preferences",
        "best_selling_categories",
        "seasonal_patterns",
        "trust_level",
        "preferred_communication"
    ]
    
    # Count discovered (not None and not empty)
    discovered_count = sum(
        1 for field in all_fields 
        if discovered_info.get(field) not in [None, "", []]
    )
    
    total_fields = len(all_fields)
    percentage = (discovered_count / total_fields) * 100
    
    # Map percentage to stars
    if percentage < 20:
        return 1  # ⭐☆☆☆☆
    elif percentage < 40:
        return 2  # ⭐⭐☆☆☆
    elif percentage < 60:
        return 3  # ⭐⭐⭐☆☆
    elif percentage < 80:
        return 4  # ⭐⭐⭐⭐☆
    else:
        return 5  # ⭐⭐⭐⭐⭐


def extract_sales_capacity_discovery(
    conversation_transcript: str,
    client: dict,
    current_discovered: dict
) -> dict:
    """
    Wyciąga informacje o sales_capacity z rozmowy używając AI
    
    Args:
        conversation_transcript: str - pełna transkrypcja rozmowy (klient + gracz)
        client: dict - dane klienta
        current_discovered: dict - obecnie odkryte capacity (sales_capacity_discovered)
    
    Returns:
        dict - nowe odkrycia per kategoria:
        {
            "Personal Care": {
                "weekly_sales_volume": 150,
                "shelf_space_facings": 12,
                "storage_capacity": 300,
                "rotation_days": 14,
                "max_order_per_sku": 24,
                "avg_products_in_category": 20,
                "discovered_date": "2025-10-30T10:00:00",
                "discovered_method": "conversation",
                "reputation_at_discovery": 35
            }
        }
    """
    if not initialize_gemini():
        return {}
    
    try:
        # Prompt dla AI do ekstrakcji structured data
        extraction_prompt = f"""
Przeanalizuj poniższą rozmowę między handlowcem a właścicielem sklepu.
Wyciągnij KONKRETNE LICZBY dotyczące sprzedaży w poszczególnych kategoriach produktów.

ROZMOWA:
{conversation_transcript}

KATEGORIE PRODUKTÓW:
- Personal Care (żele, szampony, mydła)
- Food (jogurty, sery, ketchupy)
- Home Care (płyny do naczyń, proszki)
- Snacks (chipsy, batoniki)
- Beverages (napoje, woda)

SZUKAJ INFORMACJI O:
1. weekly_sales_volume - ile sztuk sprzedaje tygodniowo w kategorii (np. "sprzedaję 150 sztuk żeli tygodniowo")
2. shelf_space_facings - ile pozycji na półce (np. "mam 12 facingów")
3. rotation_days - ile dni rotacja (np. "obraca się co 14 dni")
4. max_order_per_sku - maksymalne zamówienie na produkt (np. "max 24 sztuki na produkt")

ZWRÓĆ JSON w formacie:
{{
  "Personal Care": {{
    "weekly_sales_volume": 150,
    "shelf_space_facings": 12,
    "rotation_days": 14,
    "max_order_per_sku": 24
  }},
  "Food": {{
    ...jeśli znaleziono informacje...
  }}
}}

WAŻNE:
- Zwróć TYLKO kategorie, o których klient wspomniał konkretne liczby
- Jeśli klient nie podał liczby - NIE zgaduj! Pomiń tę kategorię
- Jeśli klient mówił ogólnie ("około 100+") - zaokrąglij do najbliższej dziesiątki
- Zwróć czysty JSON bez ```json markers

JSON:"""
        
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(extraction_prompt)
        
        # Parse JSON response
        import json
        import traceback
        
        try:
            # Safely extract text from response
            try:
                response_text = response.text.strip()
            except (AttributeError, ValueError) as e:
                print(f"⚠️ Błąd odczytu response.text w extract_sales_capacity_discovery: {e}")
                return {}
            
            # Remove markdown markers if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            extracted_data = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing error in extract_sales_capacity_discovery: {e}")
            print(f"Response text: {response_text[:200]}")
            traceback.print_exc()
            return {}
        
        # Wzbogać dane o metadane
        enriched_discoveries = {}
        reputation = client.get('reputation', 0)
        
        for category, data in extracted_data.items():
            if category not in ["Personal Care", "Food", "Home Care", "Snacks", "Beverages"]:
                continue  # Skip invalid categories
            
            # Skip if already discovered
            if category in current_discovered:
                continue
            
            # Uzupełnij brakujące pola na podstawie sales_capacity
            sales_capacity = client.get('sales_capacity', {}).get(category, {})
            
            enriched_discoveries[category] = {
                "weekly_sales_volume": data.get('weekly_sales_volume') or sales_capacity.get('weekly_sales_volume'),
                "shelf_space_facings": data.get('shelf_space_facings') or sales_capacity.get('shelf_space_facings'),
                "storage_capacity": sales_capacity.get('storage_capacity'),  # Nie odkrywane w rozmowie
                "rotation_days": data.get('rotation_days') or sales_capacity.get('rotation_days'),
                "max_order_per_sku": data.get('max_order_per_sku') or sales_capacity.get('max_order_per_sku'),
                "avg_products_in_category": sales_capacity.get('avg_products_in_category'),
                "discovered_date": datetime.now().isoformat(),
                "discovered_method": "conversation",
                "reputation_at_discovery": reputation
            }
        
        return enriched_discoveries
        
    except Exception as e:
        print(f"❌ Error in extract_sales_capacity_discovery: {e}")
        import traceback
        traceback.print_exc()
        return {}

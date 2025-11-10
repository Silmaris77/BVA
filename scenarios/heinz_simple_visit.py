"""
🎯 Heinz - Prosty Scenariusz Wizyty Handlowej

Najprostszy możliwy scenariusz:
- AI gra klienta (właściciela bistro)
- Gracz prowadzi rozmowę handlową
- Ocena i feedback tylko na końcu
"""

from typing import Dict, List, Tuple, Optional
from datetime import datetime
import google.generativeai as genai
import streamlit as st
import os


class HeinzSimpleVisitScenario:
    """Prosty scenariusz wizyty handlowej Heinz"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Args:
            api_key: Klucz API do Gemini (opcjonalny, pobierze z secrets)
        """
        if not api_key:
            api_key = self._get_api_key()
        
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
        else:
            self.model = None
            
    def _get_api_key(self) -> Optional[str]:
        """Pobiera klucz API z secrets lub environment"""
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
        
    def get_client_profile(self) -> Dict:
        """Zwraca profil klienta dla tego scenariusza"""
        return {
            "id": "michal_bistro",
            "name": "Bistro U Michała",
            "owner": "Michał Kowalski",
            "avatar": "👨‍🍳",
            "type": "bistro",
            "segment": "HoReCa małe",
            "location": "Warszawa, Mokotów",
            
            # Profil psychologiczny
            "personality": {
                "type": "pragmatyczny_oszczędny",
                "description": "Liczy każdą złotówkę, ale ceni jakość. Nie lubi agresywnej sprzedaży.",
                "openness": 6,  # 1-10, jak otwarty na nowe produkty
                "trust_level": 4,  # 1-10, początkowy poziom zaufania
            },
            
            # Obecna sytuacja
            "current_situation": {
                "ketchup_supplier": "Pudliszki",
                "monthly_ketchup_usage_kg": 8,  # ~2 butelki 5kg/miesiąc
                "current_price_per_kg": 8.50,
                "satisfaction_with_current": 7,  # 1-10
                "main_pain_point": "Klienci czasem pytają o Heinz"
            },
            
            # Co klient chce usłyszeć
            "decision_factors": [
                "Konkretna korzyść finansowa (marża)",
                "Dowód że klienci preferują Heinz",
                "Gwarancja jakości",
                "Łatwa dostępność/dostawa"
            ],
            
            # Informacje które klient może ujawnić
            "hidden_info": {
                "budget_flexibility": "Ma ~500 PLN budżetu na testy nowych produktów",
                "vip_customers": "Ma kilku stałych klientów-freaków Heinz",
                "competition": "Sąsiednie bistro ma Heinz i się chwali",
                "real_pain": "Pudliszki czasem kończą się u dostawcy"
            }
        }
    
    def start_conversation(self, client: Dict) -> str:
        """
        Rozpoczyna rozmowę - AI przedstawia się jako klient
        
        Returns:
            Początkowa wypowiedź klienta
        """
        if not self.model:
            return "Dzień dobry! Słucham?"
            
        prompt = f"""Wciel się w {client['owner']}, właściciela {client['name']}.

TWÓJ CHARAKTER:
{client['personality']['description']}

SYTUACJA:
- Używasz teraz: {client['current_situation']['ketchup_supplier']}
- Zużycie: ~{client['current_situation']['monthly_ketchup_usage_kg']} kg/miesiąc
- Jesteś zadowolony na {client['current_situation']['satisfaction_with_current']}/10

Do Twojego bistro wchodzi handlowiec Heinz.

WAŻNE - ZASADY GRY:
1. Odpowiadaj TYLKO jako właściciel bistro
2. Bądź uprzejmy ale ostrożny
3. Nie ujawniaj od razu wszystkich informacji
4. Zadawaj pytania kontrowne
5. NIE OCENIAJ handlowca - po prostu prowadź rozmowę

Przywitaj handlowca krótko (2-3 zdania). Bądź uprzejmy ale nie entuzjastyczny."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.9,
                    top_p=0.95,
                    max_output_tokens=300,
                )
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error in start_conversation: {e}")
            return "Dzień dobry! Słucham?"
    
    def continue_conversation(
        self, 
        client: Dict, 
        conversation_history: List[Dict],
        player_message: str
    ) -> str:
        """
        Kontynuuj rozmowę - AI odpowiada jako klient
        
        Args:
            client: Profil klienta
            conversation_history: Historia wiadomości [{role, content}, ...]
            player_message: Ostatnia wiadomość gracza
            
        Returns:
            Odpowiedź klienta
        """
        if not self.model:
            return "Rozumiem. A co jeszcze chciałby Pan powiedzieć?"
            
        # Zbuduj historię dla AI
        conversation_text = "\n\n".join([
            f"{'Handlowiec' if msg['role'] == 'user' else client['owner']}: {msg['content']}"
            for msg in conversation_history[:-1]  # Exclude last message (it's player_message)
        ])
        
        prompt = f"""Wciel się w {client['owner']}, właściciela {client['name']}.

TWÓJ CHARAKTER:
{client['personality']['description']}

AKTUALNA SYTUACJA:
- Obecny dostawca: {client['current_situation']['ketchup_supplier']}
- Satysfakcja: {client['current_situation']['satisfaction_with_current']}/10
- Problem: {client['current_situation']['main_pain_point']}

CO CIEBIE PRZEKONUJE:
{chr(10).join('- ' + factor for factor in client['decision_factors'])}

HISTORIA ROZMOWY DO TEJ PORY:
{conversation_text}

HANDLOWIEC WŁAŚNIE POWIEDZIAŁ:
"{player_message}"

WAŻNE ZASADY:
1. Odpowiadaj TYLKO jako właściciel - NIE OCENIAJ handlowca
2. Reaguj naturalnie na jego argumenty
3. Zadawaj pytania jeśli coś Cię zainteresuje
4. Ujawniaj informacje stopniowo (nie wszystko od razu)
5. Bądź realistyczny - prawdziwy klient nie zgadza się od razu
6. Jeśli handlowiec trafi w Twoje potrzeby - pokaż zainteresowanie
7. Jeśli nie - wyraź wątpliwości
8. Mów naturalnie, potocznie - jesteś właścicielem bistro, nie profesorem

Odpowiedz krótko (2-4 zdania) jako właściciel bistro:"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.9,
                    top_p=0.95,
                    max_output_tokens=400,
                )
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error in continue_conversation: {e}")
            return "Rozumiem. A co jeszcze chciałby Pan powiedzieć?"
    
    def evaluate_conversation(
        self,
        client: Dict,
        conversation_history: List[Dict]
    ) -> Tuple[int, str, Dict]:
        """
        Oceń całą rozmowę - DOPIERO NA KOŃCU
        
        Returns:
            (score, feedback, analysis)
            - score: 0-100
            - feedback: Tekstowy feedback w formacie FUKO
            - analysis: Słownik z detalami
        """
        if not self.model:
            return (
                50,
                "System oceny niedostępny (brak API key).",
                {"error": "no_api_key"}
            )
            
        conversation_text = "\n\n".join([
            f"{'Handlowiec' if msg['role'] == 'user' else 'Klient'}: {msg['content']}"
            for msg in conversation_history
        ])
        
        prompt = f"""Jesteś ekspertem sprzedaży B2B w branży food service.

Oceń poniższą rozmowę handlową pod kątem skuteczności sprzedaży Heinz Ketchup.

PROFIL KLIENTA:
- Typ: {client['personality']['type']}
- Opis: {client['personality']['description']}
- Co go przekonuje: {', '.join(client['decision_factors'])}
- Obecny problem: {client['current_situation']['main_pain_point']}

ROZMOWA:
{conversation_text}

OCEŃ (0-100 punktów) według kryteriów:
1. **Budowanie Relacji** (0-25): Czy handlowiec budował rapport i zaufanie?
2. **Odkrywanie Potrzeb** (0-25): Czy zadawał pytania odkrywające potrzeby?
3. **Dopasowanie Argumentów** (0-25): Czy argumenty trafiały w potrzeby klienta?
4. **Zamknięcie** (0-25): Czy próbował doprowadzić do decyzji/kolejnego kroku?

WAŻNE - Zwróć odpowiedź w CZYSTYM formacie JSON (bez markdown, bez ```json):
{{
    "score": <liczba 0-100>,
    "breakdown": {{
        "building_rapport": <0-25>,
        "discovery": <0-25>,
        "argumentation": <0-25>,
        "closing": <0-25>
    }},
    "strengths": ["mocna strona 1", "mocna strona 2"],
    "weaknesses": ["słabość 1", "słabość 2"],
    "fuko_feedback": "Feedback w formacie FUKO (Fakty-Uczucia-Konsekwencje-Oczekiwania). Używaj drugiej osoby (Ty).",
    "order_likely": true/false,
    "order_size_kg": <szacowana wielkość zamówienia w kg, 0 jeśli brak>,
    "next_steps": "Co handlowiec powinien zrobić dalej"
}}"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    top_p=0.9,
                    max_output_tokens=1000,
                )
            )
            
            # Parse JSON response
            import json
            import re
            
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            response_text = re.sub(r'```json\s*', '', response_text)
            response_text = re.sub(r'```\s*$', '', response_text)
            response_text = response_text.strip()
            
            result = json.loads(response_text)
            
            return (
                result['score'],
                result['fuko_feedback'],
                result
            )
        except Exception as e:
            print(f"Error in evaluate_conversation: {e}")
            # Fallback jeśli JSON nie zadziałał
            return (
                50,
                "Nie udało się przeanalizować rozmowy automatycznie. Spróbuj ponownie lub skontaktuj się z administratorem.",
                {"error": str(e)}
            )

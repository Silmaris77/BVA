"""
Engine dla narzędzia 6 Kapeluszy de Bono - generowanie wypowiedzi AI
"""

import random
import json
import re
from typing import Dict, List, Optional, Tuple
from data.six_hats_templates import HATS_DEFINITIONS, HATS_CONFLICTS

class SixHatsEngine:
    """Silnik generujący wypowiedzi poszczególnych kapeluszy"""
    
    def __init__(self):
        self.evaluator = None
        self._init_evaluator()
    
    def _init_evaluator(self):
        """Inicjalizuje evaluator AI"""
        try:
            from utils.ai_exercises import AIExerciseEvaluator
            self.evaluator = AIExerciseEvaluator()
        except Exception as e:
            print(f"Nie udało się zainicjalizować AI: {e}")
    
    def generate_hat_response(
        self, 
        hat_color: str, 
        problem: str,
        context: str,
        previous_messages: List[Dict],
        allow_conflict: bool = True
    ) -> Dict:
        """
        Generuje wypowiedź dla danego kapeluszy
        
        Args:
            hat_color: kolor kapeluszy (white/red/black/yellow/green/blue)
            problem: opisany problem do rozwiązania
            context: dodatkowy kontekst użytkownika
            previous_messages: poprzednie wiadomości w sesji
            allow_conflict: czy pozwolić na konflikt z poprzednimi kapeluszami
            
        Returns:
            Dict z wypowiedzią i metadanymi
        """
        hat_def = HATS_DEFINITIONS.get(hat_color, HATS_DEFINITIONS["white"])
        
        # Sprawdź czy powinien być konflikt
        conflict_target = None
        if allow_conflict and len(previous_messages) > 0:
            conflict_target = self._check_for_conflict(hat_color, previous_messages)
        
        # Zbierz poprzednie wypowiedzi dla kontekstu
        previous_summary = self._summarize_previous(previous_messages, limit=3)
        
        # Generuj prompt
        if conflict_target:
            response = self._generate_conflict_response(
                hat_color, hat_def, problem, context, conflict_target, previous_messages
            )
        else:
            response = self._generate_normal_response(
                hat_color, hat_def, problem, context, previous_summary
            )
        
        return {
            "hat": hat_color,
            "hat_name": hat_def["name"],
            "role": hat_def["role"],
            "content": response,
            "is_conflict": conflict_target is not None,
            "conflict_with": conflict_target
        }
    
    def _check_for_conflict(self, current_hat: str, previous_messages: List[Dict]) -> Optional[str]:
        """Sprawdza czy powinien wystąpić konflikt"""
        for conflict_def in HATS_CONFLICTS:
            if current_hat in conflict_def["hats"]:
                # Znajdź drugi kapelusz z konfliktu
                other_hat = [h for h in conflict_def["hats"] if h != current_hat][0]
                
                # Sprawdź czy ten kapelusz już się wypowiadał
                recent_hats = [msg["hat"] for msg in previous_messages[-3:] if msg.get("hat")]
                if other_hat in recent_hats:
                    # Losuj czy wystąpi konflikt
                    if random.random() < conflict_def["probability"]:
                        return other_hat
        
        return None
    
    def _summarize_previous(self, messages: List[Dict], limit: int = 3) -> str:
        """Tworzy podsumowanie poprzednich wypowiedzi"""
        if not messages:
            return "To początek sesji."
        
        recent = messages[-limit:]
        summary_parts = []
        
        for msg in recent:
            if msg.get("hat"):
                hat_name = HATS_DEFINITIONS[msg["hat"]]["name"]
                content_short = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
                summary_parts.append(f"{hat_name}: {content_short}")
        
        return "\n".join(summary_parts)
    
    def _generate_normal_response(
        self,
        hat_color: str,
        hat_def: Dict,
        problem: str,
        context: str,
        previous_summary: str
    ) -> str:
        """Generuje normalną wypowiedź kapeluszy"""
        
        # Skrócony, efektywny prompt
        context_line = f'KONTEKST: {context}\n' if context else ''
        prompt = f"""Jesteś {hat_def["role"]} w zespole 6 Kapeluszy de Bono.

PERSPEKTYWA: {hat_def["description"]}
PROBLEM: {problem}
{context_line}DOTYCHCZAS: {previous_summary}

Wypowiedź (2-3 zdania) z perspektywy {hat_def["name"]}:"""

        try:
            if self.evaluator and hasattr(self.evaluator, 'gemini_model'):
                response = self.evaluator.gemini_model.generate_content(prompt)
                if response and response.text:
                    return response.text.strip()
        except Exception as e:
            print(f"Błąd generowania AI: {e}")
        
        # Fallback
        return self._generate_fallback_response(hat_color, hat_def, problem)
    
    def _generate_conflict_response(
        self,
        hat_color: str,
        hat_def: Dict,
        problem: str,
        context: str,
        conflict_with: str,
        previous_messages: List[Dict]
    ) -> str:
        """Generuje wypowiedź z konfliktem"""
        
        # Znajdź ostatnią wypowiedź kapeluszy z którym jest konflikt
        conflict_message = None
        for msg in reversed(previous_messages):
            if msg.get("hat") == conflict_with:
                conflict_message = msg["content"]
                break
        
        conflict_hat_def = HATS_DEFINITIONS[conflict_with]
        
        # Skrócony prompt dla konfliktu
        prompt = f"""Jesteś {hat_def["role"]} ({hat_def["name"]}) w zespole.

{conflict_hat_def["name"]} powiedział: "{conflict_message}"

Zareaguj z własnej perspektywy ({hat_def["description"]}). Konstruktywnie, ale pokaż różnicę zdań. 2-3 zdania:"""

        try:
            if self.evaluator and hasattr(self.evaluator, 'gemini_model'):
                response = self.evaluator.gemini_model.generate_content(prompt)
                if response and response.text:
                    return response.text.strip()
        except Exception as e:
            print(f"Błąd generowania AI: {e}")
        
        # Fallback - wybierz losowy konflikt z szablonu
        for conflict_def in HATS_CONFLICTS:
            if set(conflict_def["hats"]) == {hat_color, conflict_with}:
                return random.choice(conflict_def["examples"]).split("\n")[0]
        
        return self._generate_fallback_response(hat_color, hat_def, problem)
    
    def _generate_fallback_response(self, hat_color: str, hat_def: Dict, problem: str) -> str:
        """Generuje prostą fallback odpowiedź"""
        
        fallbacks = {
            "white": f"Potrzebujemy więcej danych o: {problem}. Jakie fakty już znamy?",
            "red": f"Mam przeczucie co do tego problemu. Intuicja podpowiada mi, że warto się temu przyjrzeć.",
            "black": f"Widzę potencjalne ryzyka w tym pomyśle. Co może pójść nie tak?",
            "yellow": f"To interesująca szansa! Widzę potencjał w rozwiązaniu tego problemu.",
            "green": f"A gdyby spróbować zupełnie innego podejścia? Pomyślmy kreatywnie!",
            "blue": f"Podsumujmy dotychczasowe ustalenia i zaplanujmy następne kroki."
        }
        
        return fallbacks.get(hat_color, "Dobre pytanie do rozważenia.")
    
    def generate_synthesis(
        self,
        problem: str,
        context: str,
        all_messages: List[Dict]
    ) -> Dict:
        """
        Generuje syntezę całej sesji z top 3 pomysłami
        
        Returns:
            Dict z podsumowaniem, pomysłami, planem działania
        """
        
        # Zbierz wszystkie wypowiedzi kapeluszy
        hats_summary = {}
        for msg in all_messages:
            if msg.get("hat") and msg["hat"] != "blue":
                hat_name = HATS_DEFINITIONS[msg["hat"]]["name"]
                if hat_name not in hats_summary:
                    hats_summary[hat_name] = []
                hats_summary[hat_name].append(msg["content"])
        
        # Przygotuj podsumowanie dla AI
        summary_text = "\n\n".join([
            f"{hat}:\n" + "\n".join([f"- {content}" for content in contents])
            for hat, contents in hats_summary.items()
        ])
        
        # Skrócony prompt dla syntezy
        context_line = f'KONTEKST: {context}\n' if context else ''
        prompt = f"""Sesja 6 Kapeluszy de Bono.

PROBLEM: {problem}
{context_line}
DYSKUSJA:
{summary_text}

JSON (bez markdown):
{{
    "summary": "Podsumowanie (3 zdania)",
    "key_insights": ["insight1", "insight2", "insight3"],
    "top_ideas": [
        {{"idea": "Rozwiązanie 1", "pros": "Zalety", "cons": "Wady", "feasibility": 1-10}},
        {{"idea": "Rozwiązanie 2", "pros": "Zalety", "cons": "Wady", "feasibility": 1-10}},
        {{"idea": "Rozwiązanie 3", "pros": "Zalety", "cons": "Wady", "feasibility": 1-10}}
    ],
    "next_steps": ["krok1", "krok2", "krok3"],
    "recommendation": "Główna rekomendacja (1 zdanie)"
}}"""

        try:
            if self.evaluator and hasattr(self.evaluator, 'gemini_model'):
                response = self.evaluator.gemini_model.generate_content(prompt)
                if response and response.text:
                    content = response.text.strip()
                    
                    # Usuń markdown
                    if content.startswith("```json"):
                        content = content.replace("```json", "").replace("```", "").strip()
                    elif content.startswith("```"):
                        content = content.replace("```", "").strip()
                    
                    # Wydobądź JSON
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
        
        except Exception as e:
            print(f"Błąd generowania syntezy: {e}")
        
        # Fallback
        return {
            "summary": "Zespół przeprowadził sesję kreatywną używając metody 6 Kapeluszy.",
            "key_insights": [
                "Różne perspektywy pomogły zobaczyć problem kompleksowo",
                "Zidentyfikowano zarówno szanse jak i ryzyka",
                "Wygenerowano kilka interesujących pomysłów"
            ],
            "top_ideas": [
                {
                    "idea": "Rozwiązanie wymagające dalszej analizy",
                    "pros": "Może przynieść korzyści",
                    "cons": "Wymaga zasobów",
                    "feasibility": 5
                }
            ],
            "next_steps": [
                "Przeanalizować szczegółowo najlepszy pomysł",
                "Skonsultować z zespołem",
                "Przygotować plan wdrożenia"
            ],
            "recommendation": "Warto kontynuować prace nad tym problemem z uwzględnieniem różnych perspektyw."
        }

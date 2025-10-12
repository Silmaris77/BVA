"""
Test nowego typu ćwiczenia AI - Generated Case Study
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.ai_exercises import AIExerciseEvaluator

def test_generated_case():
    """Test generowania i oceny case study"""
    
    evaluator = AIExerciseEvaluator()
    
    print("🎯 Test 1: Generowanie case study")
    print("="*50)
    
    # Test generowania case study
    case_data = evaluator.generate_case_study(
        lesson_context="Conversational Intelligence - neurobiologia rozmowy", 
        difficulty_level="medium"
    )
    
    print(f"📋 Tytuł: {case_data.get('title', 'Brak tytułu')}")
    print(f"🏢 Kontekst: {case_data.get('company_context', 'Brak kontekstu')}")
    print(f"📖 Sytuacja: {case_data.get('situation', 'Brak opisu')}")
    print(f"🎯 Zadanie: {case_data.get('task', 'Brak zadania')}")
    print(f"⏱️ Czas: {case_data.get('estimated_time', 'Nie określono')}")
    print(f"🔧 Tryb: {'Demo' if case_data.get('generated_at') == 'demo_mode' else 'AI'}")
    
    print("\n🎯 Test 2: Ocena odpowiedzi użytkownika")
    print("="*50)
    
    # Przykładowa odpowiedź użytkownika
    user_response = """
    W tej sytuacji widzę, że Anna stoi przed wyzwaniem przekazania stresującej informacji. 
    Zamiast po prostu ogłosić złą wiadomość, powinna zastosować Poziom III komunikacji.
    
    Proponuję następujący scenariusz:
    
    1. Anna zaczyna od uznania ciężkiej pracy zespołu
    2. Pyta zespół o ich obecne odczucia i wyzwania
    3. Razem z zespołem szuka rozwiązań dla nowego deadline'u
    4. Tworzy plan działania z podziałem odpowiedzialności
    
    To podejście aktywuje oksytocynę zamiast kortyzolu i buduje zaufanie.
    """
    
    # Konfiguracja ćwiczenia
    exercise_config = {
        'exercise_type': 'generated_case',
        'generated_case_data': case_data
    }
    
    # Ocena odpowiedzi
    evaluation = evaluator.evaluate_exercise(
        exercise_config=exercise_config,
        user_response=user_response,
        lesson_context="Conversational Intelligence - neurobiologia rozmowy"
    )
    
    print(f"📊 Ogólna ocena: {evaluation.get('overall_score', 'Brak')}/10")
    print(f"💬 Feedback: {evaluation.get('feedback', 'Brak feedback')}")
    print(f"✅ Mocne strony: {evaluation.get('strong_points', [])}")
    print(f"📈 Obszary poprawy: {evaluation.get('improvement_areas', [])}")
    
    return case_data, evaluation

if __name__ == "__main__":
    print("🧪 Test nowego typu ćwiczenia: Generated Case Study")
    print("="*60)
    
    try:
        case, eval_result = test_generated_case()
        print("\n✅ Test zakończony pomyślnie!")
        print(f"📋 Wygenerowano case: {case.get('title', 'Brak tytułu')}")
        print(f"📊 Ocena: {eval_result.get('overall_score', 'Brak')}/10")
        
    except Exception as e:
        print(f"\n❌ Błąd podczas testu: {str(e)}")
        import traceback
        traceback.print_exc()
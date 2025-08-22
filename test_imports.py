#!/usr/bin/env python3
"""
Test importów neurolidera
"""

def test_imports():
    print("🧠 Testowanie importów neurolidera...")
    
    try:
        # Test importu danych neurolidera
        from data.neuroleader_details import neuroleader_details
        print(f"✅ neuroleader_details: {len(neuroleader_details)} typów")
        
        # Test importu pytań testowych
        from data.neuroleader_test_questions import NEUROLEADER_TYPES, TEST_QUESTIONS
        print(f"✅ NEUROLEADER_TYPES: {len(NEUROLEADER_TYPES)} typów")
        print(f"✅ TEST_QUESTIONS: {len(TEST_QUESTIONS)} pytań")
        
        # Test importu z config
        from config.settings import NEUROLEADER_TYPES as config_types
        print(f"✅ Config NEUROLEADER_TYPES: {len(config_types)} typów")
        
        # Test funkcji profilu
        from views.profile import show_neuroleader_test_section, show_current_neuroleader_type
        print("✅ Funkcje profilu neurolidera zaimportowane")
        
        print("\n🎉 Wszystkie importy neurolidera działają!")
        return True
        
    except Exception as e:
        print(f"❌ Błąd importu: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_imports()

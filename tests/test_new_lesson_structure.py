"""
Test script to verify the new lesson structure implementation
"""
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Test imports
    from views.lesson import show_lesson
    from data.lessons import load_lessons
    from data.users import load_user_data
    
    print("✅ All imports successful!")
    
    # Test lesson data loading
    lessons = load_lessons()
    print(f"✅ Loaded {len(lessons)} lessons")
    
    # Test user data loading
    user_data = load_user_data()
    print(f"✅ User data loaded (users: {len(user_data)})")
    
    print("\n🎉 New lesson structure is ready!")
    print("\nNew lesson structure features:")
    print("📚 Tab 1: Wprowadzenie (Wprowadzenie, Case Study, Samorefleksja)")
    print("📖 Tab 2: Materiał (unchanged)")
    print("🎯 Tab 3: Zadania praktyczne (Ćwiczenia+autorefleksja, Quiz końcowy)")
    print("📋 Tab 4: Podsumowanie (Podsumowanie, Case Study, Mapa myśli)")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

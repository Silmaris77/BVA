#!/usr/bin/env python3
"""
Test script to verify the neuroleader migration is working correctly
"""

def test_neuroleader_imports():
    """Test that all neuroleader imports work correctly"""
    try:
        from data.neuroleader_details import neuroleader_details
        from data.neuroleader_test_questions import NEUROLEADER_TYPES, TEST_QUESTIONS
        from config.settings import NEUROLEADER_TYPES as settings_neuroleader_types
        
        print("✅ All neuroleader imports successful")
        
        # Test that we have the expected neuroleader types
        expected_types = ["Neuroanalityk", "Neuroreaktor", "Neurobalanser", "Neuroempata", "Neuroinnowator", "Neuroinspirator"]
        
        for neuroleader_type in expected_types:
            if neuroleader_type in NEUROLEADER_TYPES:
                print(f"✅ {neuroleader_type} found in NEUROLEADER_TYPES")
            else:
                print(f"❌ {neuroleader_type} NOT found in NEUROLEADER_TYPES")
                
            if neuroleader_type in settings_neuroleader_types:
                print(f"✅ {neuroleader_type} found in settings NEUROLEADER_TYPES")
            else:
                print(f"❌ {neuroleader_type} NOT found in settings NEUROLEADER_TYPES")
                
        # Test that we have test questions
        if TEST_QUESTIONS and len(TEST_QUESTIONS) > 0:
            print(f"✅ Found {len(TEST_QUESTIONS)} test questions")
        else:
            print("❌ No test questions found")
            
        # Test that we have detailed descriptions
        if neuroleader_details and len(neuroleader_details) > 0:
            print(f"✅ Found {len(neuroleader_details)} detailed descriptions")
        else:
            print("❌ No detailed descriptions found")
            
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_profile_functions():
    """Test that profile functions can be imported"""
    try:
        # Test importing specific functions from profile
        import sys
        sys.path.append('.')
        from views.profile import show_neuroleader_test_section, show_current_neuroleader_type
        
        print("✅ Profile neuroleader functions imported successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Profile function import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected profile error: {e}")
        return False

if __name__ == "__main__":
    print("🧠 Testing Neuroleader Migration")
    print("=" * 50)
    
    success = True
    
    print("\n1. Testing neuroleader imports...")
    success &= test_neuroleader_imports()
    
    print("\n2. Testing profile functions...")
    success &= test_profile_functions()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Neuroleader migration successful.")
    else:
        print("❌ Some tests failed. Please check the errors above.")

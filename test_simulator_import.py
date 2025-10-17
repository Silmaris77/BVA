"""Quick test of simulator import"""
import sys
print("Python executable:", sys.executable)
print("Python version:", sys.version)

print("\n1. Testing basic imports...")
import streamlit as st
print("✅ Streamlit OK")

print("\n2. Testing AIExerciseEvaluator...")
try:
    from utils.ai_exercise_evaluator import AIExerciseEvaluator
    print("✅ AIExerciseEvaluator OK")
except Exception as e:
    print(f"❌ AIExerciseEvaluator ERROR: {e}")

print("\n3. Testing simulator import...")
try:
    from views.simulators.business_simulator import show_business_simulator
    print("✅ Business Simulator OK")
except Exception as e:
    print(f"❌ Business Simulator ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ All tests completed!")

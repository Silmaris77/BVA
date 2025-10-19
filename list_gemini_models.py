"""
Lista dostępnych modeli Google Gemini
"""

import google.generativeai as genai
import os

# Konfiguruj API key
try:
    import streamlit as st
    api_key = st.secrets.get("GOOGLE_API_KEY")
except:
    api_key = "AIzaSyDJu4fJoICZCe9O8shCN18SSq9t_gFH8nM"  # Z pliku secrets.toml

genai.configure(api_key=api_key)

print("="*60)
print("   DOSTĘPNE MODELE GOOGLE GEMINI")
print("="*60)
print()

try:
    print("🔍 Pobieranie listy modeli...")
    models = genai.list_models()
    
    print("\n📋 Modele obsługujące generateContent:\n")
    
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Display name: {model.display_name}")
            print(f"   Description: {model.description[:100]}...")
            print()
    
except Exception as e:
    print(f"❌ Błąd: {e}")
    import traceback
    traceback.print_exc()

print("="*60)
print("💡 Użyj jednego z powyższych modeli w konfiguracji!")
print("="*60)

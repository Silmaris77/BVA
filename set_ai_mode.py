"""
Skrypt do automatycznej zmiany trybu oceny Business Games na AI (Gemini)
"""

import json
import os
from datetime import datetime

def set_evaluation_mode_to_ai():
    """Zmienia tryb oceny na AI"""
    
    settings_file = "config/business_games_active_mode.json"
    
    print("🔧 Zmiana trybu oceny Business Games...")
    print(f"📁 Plik: {settings_file}\n")
    
    # Sprawdź czy katalog istnieje
    os.makedirs(os.path.dirname(settings_file), exist_ok=True)
    
    # Nowa konfiguracja
    config = {
        "evaluation_mode": "ai",
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_by": "auto_script"
    }
    
    # Zapisz
    try:
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("✅ Sukces! Tryb oceny zmieniony na: AI (Gemini)")
        print(f"⏰ Data zmiany: {config['updated_at']}")
        print("\n" + "="*60)
        print("📋 SZCZEGÓŁY KONFIGURACJI:")
        print("="*60)
        print(f"🤖 Tryb: AI (Google Gemini)")
        print(f"📦 Model: gemini-1.5-flash")
        print(f"🔑 API Key: Skonfigurowany w st.secrets")
        print(f"💰 Koszt: ~$0.01-0.03 za ocenę")
        print("\n" + "="*60)
        print("🎯 CO DALEJ:")
        print("="*60)
        print("1. ✅ Tryb został zmieniony")
        print("2. 🔄 Uruchom ponownie aplikację Streamlit")
        print("3. 🎮 Przejdź do Business Games")
        print("4. 📝 Wykonaj nowy kontrakt")
        print("5. 📜 Zobacz szczegółowy feedback od AI w zakładce Historia!")
        print("\n🎉 Od teraz wszystkie nowe kontrakty będą oceniane przez Gemini AI!")
        
        return True
        
    except Exception as e:
        print(f"❌ Błąd: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("   ZMIANA TRYBU OCENY NA AI (GEMINI)")
    print("="*60)
    print()
    
    success = set_evaluation_mode_to_ai()
    
    if success:
        print("\n✨ Gotowe! Teraz możesz cieszyć się oceną AI! ✨")
    else:
        print("\n⚠️ Wystąpił problem. Spróbuj zmienić tryb ręcznie w panelu admina.")

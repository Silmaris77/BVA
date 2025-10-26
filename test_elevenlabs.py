"""Test ElevenLabs TTS"""
import streamlit as st

# Ładuj secrets
api_key = st.secrets.get("API_KEYS", {}).get("elevenlabs", "")

print(f"Klucz API: {api_key[:20]}..." if api_key else "BRAK KLUCZA")

if not api_key:
    print("❌ Brak klucza ElevenLabs w secrets!")
    exit(1)

try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs import VoiceSettings
    print("✅ Import ElevenLabs OK")
    
    client = ElevenLabs(api_key=api_key)
    print("✅ Klient ElevenLabs utworzony")
    
    # Test prostej generacji
    print("🎤 Testuję generację audio...")
    
    audio_generator = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB",  # Adam - polski głos
        text="Witaj, jestem Mark. To jest test głosu.",
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
            style=0.5,
            use_speaker_boost=True
        )
    )
    
    # Zbierz audio
    audio_bytes = b"".join(audio_generator)
    
    print(f"✅ Audio wygenerowane! Rozmiar: {len(audio_bytes)} bajtów")
    print("🎉 ElevenLabs działa poprawnie!")
    
except Exception as e:
    print(f"❌ BŁĄD: {e}")
    import traceback
    traceback.print_exc()

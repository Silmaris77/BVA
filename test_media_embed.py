"""
Test funkcjonalności osadzonych mediów
"""
import streamlit as st
from utils.media_embed import *

st.title("🎥🎧 Test Osadzonych Mediów")

st.subheader("🎬 Test YouTube Video - Conversational Intelligence")
youtube_content = embed_youtube_video("zWBujW9o2Hc", title="Inteligencja konwersacyjna w pigułce")
st.markdown(youtube_content, unsafe_allow_html=True)

st.subheader("🎧 Test YouTube Audio - Podcast")
podcast_content = embed_youtube_video("1eram4uEQ58", title="Podcast - Wprowadzenie do Conversational Intelligence")
st.markdown(podcast_content, unsafe_allow_html=True)

st.subheader("📋 Test Renderowania z Media Embed")
test_section = {
    "title": "Test Media Section",
    "content": "EMBED_YOUTUBE:zWBujW9o2Hc",
    "embed_type": "youtube",
    "embed_id": "zWBujW9o2Hc",
    "description": "To jest test osadzonego video"
}

st.markdown("### Test Media Section")
render_embedded_content(test_section['content'], test_section)
"""
Test sprawdzający gdzie renderowane są sekcje learning w aplikacji
"""
import streamlit as st
from data.lessons import load_lessons

def test_find_learning_renderer():
    """Testuje gdzie jest renderowana sekcja learning"""
    
    # Sprawdź czy aplikacja ma dostęp do lekcji
    lessons = load_lessons()
    lesson_11 = lessons.get('NEUROLEADERSHIP_LESSON_11', {})
    
    st.title("🧪 Test Renderowania Learning")
    
    if lesson_11:
        st.success(f"✅ Znaleziono lekcję: {lesson_11.get('title', 'Bez tytułu')}")
        
        # Sprawdź strukturę
        if 'sections' in lesson_11:
            sections = lesson_11['sections']
            st.write("📋 Sekcje w lekcji:", list(sections.keys()))
            
            if 'learning' in sections:
                learning = sections['learning']
                st.write("🎯 Struktura learning:", list(learning.keys()))
                
                if 'tabs' in learning:
                    tabs = learning['tabs']
                    st.write(f"📁 Liczba tabs: {len(tabs)}")
                    
                    for i, tab in enumerate(tabs):
                        st.write(f"Tab {i}: {tab.get('name', 'Bez nazwy')}")
                        if 'sections' in tab:
                            sections_count = len(tab['sections'])
                            st.write(f"  - Sekcje: {sections_count}")
                            
                            # Sprawdź pierwszy content
                            if sections_count > 0:
                                first_section = tab['sections'][0]
                                content = first_section.get('content', '')
                                if content.startswith('EMBED_'):
                                    st.write(f"  - Zawiera osadzone media: {content[:30]}...")
                                else:
                                    st.write(f"  - Zawiera tekst: {len(content)} znaków")
                else:
                    st.warning("❌ Brak tabs w learning")
            else:
                st.warning("❌ Brak learning w sections")
        else:
            st.error("❌ Brak sections w lekcji")
    else:
        st.error("❌ Nie znaleziono lekcji 11")

if __name__ == "__main__":
    test_find_learning_renderer()
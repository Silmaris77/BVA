#!/usr/bin/env python3
"""
Przywrócenie struktury tabs dla lekcji 11 z linkiem do podcastu
"""

import json
import os

def restore_lesson_11_tabs():
    lesson_file = "data/lessons/11. Od słów do zaufania - Conversational Intelligence.json"
    
    # Backup
    with open(lesson_file, 'r', encoding='utf-8') as f:
        lesson = json.load(f)
    
    # Utwórz backup
    backup_file = lesson_file.replace('.json', '_backup_sections.json')
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(lesson, f, ensure_ascii=False, indent=2)
    print(f"✅ Backup zapisany: {backup_file}")
    
    # Pobierz istniejące sekcje z learning
    existing_sections = lesson['sections']['learning']['sections']
    
    # Przekształć na strukturę tabs
    lesson['sections']['learning'] = {
        "tabs": [
            {
                "id": "tekst",
                "title": "📚 Tekst",
                "icon": "📚",
                "sections": existing_sections  # Użyj istniejące sekcje
            },
            {
                "id": "podcast", 
                "title": "🎧 Podcast",
                "icon": "🎧",
                "sections": [
                    {
                        "title": "🎧 Podcast - Conversational Intelligence",
                        "content": f"""
                        <div style='background: linear-gradient(135deg, #1a237e 0%, #3949ab 100%); padding: 25px; border-radius: 12px; margin: 20px 0; color: white;'>
                            <div style='background: rgba(255,255,255,0.95); padding: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color: #2c3e50;'>
                                <div style='text-align: center; margin-bottom: 25px; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; color: white;'>
                                    <h3 style='margin: 0; font-size: 1.3rem;'>🎧 Podcast Edition</h3>
                                    <p style='margin: 10px 0 0 0; font-size: 1.1rem; opacity: 0.9;'>Wprowadzenie do Inteligencji Konwersacyjnej</p>
                                </div>
                                
                                <div style='background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); padding: 20px; border-radius: 8px; margin: 20px 0;'>
                                    <h4 style='color: #2e7d32; margin-bottom: 15px; text-align: center;'>🎯 Posłuchaj wprowadzenia do koncepcji Judith Glaser</h4>
                                    <p style='color: #424242; line-height: 1.7; text-align: center; margin-bottom: 20px;'>
                                        Poznaj fundamenty Conversational Intelligence® w formacie audio. 
                                        Dowiedz się, jak rozmowy kształtują neurochemię mózgu i wpływają na jakość relacji.
                                    </p>
                                </div>
                                
                                <div style='text-align: center; margin: 30px 0;'>
                                    <a href='https://music.youtube.com/watch?v=1eram4uEQ58&list=MLPT' 
                                       target='_blank' 
                                       style='display: inline-block; background: #ff0000; color: white; padding: 15px 30px; border-radius: 30px; text-decoration: none; font-weight: bold; font-size: 1.1rem; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(255,0,0,0.3);'
                                       onmouseover='this.style.transform="scale(1.05)"; this.style.boxShadow="0 6px 20px rgba(255,0,0,0.4)"' 
                                       onmouseout='this.style.transform="scale(1)"; this.style.boxShadow="0 4px 15px rgba(255,0,0,0.3)"'>
                                        🎶 Słuchaj na YouTube Music
                                    </a>
                                </div>
                                
                                <div style='background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); padding: 20px; border-radius: 8px; margin: 20px 0;'>
                                    <h4 style='color: #e65100; margin-bottom: 15px;'>🎯 Kluczowe tematy:</h4>
                                    <div style='background: white; padding: 20px; border-radius: 8px;'>
                                        <ul style='color: #424242; line-height: 1.8; margin: 0;'>
                                            <li><strong>Neurobiologia rozmów</strong> - jak oksytocyna i kortyzol wpływają na komunikację</li>
                                            <li><strong>Trzy poziomy konwersacji</strong> - od transakcyjnych do transformacyjnych</li>
                                            <li><strong>Model TRUST</strong> - narzędzie budowania zaufania w relacjach</li>
                                            <li><strong>Praktyczne techniki C-IQ</strong> - jak prowadzić rozmowy poziomu III</li>
                                        </ul>
                                    </div>
                                </div>
                                
                                <div style='background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); padding: 20px; border-radius: 8px; margin: 20px 0;'>
                                    <h4 style='color: #7b1fa2; margin-bottom: 15px;'>📝 Po odsłuchaniu:</h4>
                                    <div style='background: white; padding: 20px; border-radius: 8px;'>
                                        <p style='color: #424242; line-height: 1.7; margin-bottom: 15px;'>
                                            Będziesz rozumieć, dlaczego Judith Glaser mówi, że <strong>"wszystko dzieje się poprzez rozmowy"</strong> 
                                            i jak możesz wykorzystać tę wiedzę w codziennym przywództwie.
                                        </p>
                                        <p style='color: #7b1fa2; font-weight: 600; margin: 0;'>
                                            🌟 Każda rozmowa to szansa na budowanie zaufania i wspólnego sukcesu!
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        """
                    }
                ]
            },
            {
                "id": "video",
                "title": "🎬 Video", 
                "icon": "🎬",
                "sections": [
                    {
                        "title": "🎬 Film - Conversational Intelligence w praktyce",
                        "content": """
                        <div style='background: linear-gradient(135deg, #c62828 0%, #f44336 100%); padding: 25px; border-radius: 12px; margin: 20px 0; color: white;'>
                            <div style='background: rgba(255,255,255,0.95); padding: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color: #2c3e50;'>
                                <div style='text-align: center; margin-bottom: 25px; padding: 20px; background: linear-gradient(135deg, #d32f2f 0%, #f44336 100%); border-radius: 8px; color: white;'>
                                    <h3 style='margin: 0; font-size: 1.3rem;'>🎬 Video Edition</h3>
                                    <p style='margin: 10px 0 0 0; font-size: 1.1rem; opacity: 0.9;'>Conversational Intelligence w obrazie i dźwięku</p>
                                </div>
                                
                                <p style='color: #2c3e50; line-height: 1.8; font-size: 1.1rem; margin-bottom: 20px; text-align: center;'>
                                    Obejrzyj <strong>dynamiczną prezentację koncepcji Judith Glaser</strong> w 10-minutowym filmie! 
                                    Poznaj rewolucyjne odkrycie dotyczące tego, jak rozmowy kształtują naszą rzeczywistość.
                                </p>
                                
                                <div style='text-align: center; margin: 30px 0;'>
                                    <a href='https://youtu.be/zWBujW9o2Hc' 
                                       target='_blank' 
                                       style='display: inline-block; background: #ff0000; color: white; padding: 15px 30px; border-radius: 30px; text-decoration: none; font-weight: bold; font-size: 1.1rem; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(255,0,0,0.3);'
                                       onmouseover='this.style.transform="scale(1.05)"; this.style.boxShadow="0 6px 20px rgba(255,0,0,0.4)"' 
                                       onmouseout='this.style.transform="scale(1)"; this.style.boxShadow="0 4px 15px rgba(255,0,0,0.3)"'>
                                        🎬 Oglądaj na YouTube
                                    </a>
                                </div>
                                
                                <div style='background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); padding: 20px; border-radius: 8px; margin: 20px 0;'>
                                    <h4 style='color: #e65100; margin-bottom: 15px;'>🎥 Główne tematy filmu:</h4>
                                    <div style='background: white; padding: 20px; border-radius: 8px;'>
                                        <ul style='color: #424242; line-height: 1.8; margin: 0;'>
                                            <li><strong>Porwanie amygdali</strong> - jak mózg reaguje na zagrożenie w rozmowie</li>
                                            <li><strong>Ścieżka strachu vs. zaufania</strong> - neurobiologia komunikacji</li>
                                            <li><strong>Trzy poziomy rozmów</strong> - praktyczne różnice i zastosowania</li>
                                            <li><strong>Transformacja zespołu</strong> - przejście z "ja" na "my"</li>
                                        </ul>
                                    </div>
                                </div>
                                
                                <div style='background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); padding: 20px; border-radius: 8px; margin: 20px 0;'>
                                    <h4 style='color: #2e7d32; margin-bottom: 15px;'>💡 Kluczowy cytat z filmu:</h4>
                                    <div style='background: white; padding: 20px; border-radius: 8px; text-align: center;'>
                                        <blockquote style='color: #2e7d32; font-style: italic; font-size: 1.2rem; margin: 0; border: none; padding: 0;'>
                                            "Klucz do sukcesu nie leży w tym co mówimy,<br>ale w tym jak to robimy"
                                        </blockquote>
                                    </div>
                                </div>
                            </div>
                        </div>
                        """
                    }
                ]
            }
        ]
    }
    
    # Zapisz zaktualizowaną lekcję
    with open(lesson_file, 'w', encoding='utf-8') as f:
        json.dump(lesson, f, ensure_ascii=False, indent=2)
    
    print("✅ Struktura tabs przywrócona!")
    print("✅ Link do podcastu dodany!")
    print(f"🎧 Podcast: https://music.youtube.com/watch?v=1eram4uEQ58&list=MLPT")
    
    # Sprawdź strukturę
    print("\n📊 Nowa struktura:")
    for i, tab in enumerate(lesson['sections']['learning']['tabs']):
        print(f"  Tab {i+1}: {tab['title']} ({len(tab['sections'])} sekcji)")

if __name__ == "__main__":
    restore_lesson_11_tabs()
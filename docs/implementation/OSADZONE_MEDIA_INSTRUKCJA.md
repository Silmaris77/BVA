# 🎥🎧 Implementacja Osadzonych Mediów w Aplikacji - Podcasts i Videos

## 🎯 Cel
Zamiana zewnętrznych linków na osadzone okienka dla podcastów i filmów bezpośrednio w aplikacji Streamlit.

## 📊 Aktualne vs. Docelowe Rozwiązanie

### ❌ Aktualne Rozwiązanie
- Linki zewnętrzne do platform (Spotify, YouTube, SoundCloud)
- Użytkownik musi opuścić aplikację
- Utrata engagement i kontekstu nauki

### ✅ Docelowe Rozwiązanie  
- Osadzone okienka bezpośrednio w aplikacji
- Odtwarzanie bez opuszczania strony
- Lepsze UX i zachowanie kontekstu

## 🔧 Implementacja dla Różnych Platform

### 1. 🎧 Podcasts - Osadzanie Audio

#### Spotify Embed
```python
def embed_spotify_podcast(episode_id):
    """Osadza podcast ze Spotify"""
    spotify_embed = f"""
    <iframe src="https://open.spotify.com/embed/episode/{episode_id}?utm_source=generator" 
            width="100%" 
            height="352" 
            frameBorder="0" 
            allowfullscreen="" 
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
            loading="lazy">
    </iframe>
    """
    return spotify_embed

# Użycie w Streamlit
st.markdown(embed_spotify_podcast("episode_id"), unsafe_allow_html=True)
```

#### SoundCloud Embed
```python
def embed_soundcloud_audio(track_url):
    """Osadza audio z SoundCloud"""
    soundcloud_embed = f"""
    <iframe width="100%" 
            height="166" 
            scrolling="no" 
            frameborder="no" 
            allow="autoplay" 
            src="https://w.soundcloud.com/player/?url={track_url}&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true">
    </iframe>
    """
    return soundcloud_embed
```

#### Apple Podcasts Embed
```python
def embed_apple_podcast(podcast_id, episode_id=None):
    """Osadza podcast z Apple Podcasts"""
    base_url = f"https://embed.podcasts.apple.com/us/podcast/id{podcast_id}"
    if episode_id:
        base_url += f"?i={episode_id}"
    
    apple_embed = f"""
    <iframe allow="autoplay *; encrypted-media *; fullscreen *; clipboard-write" 
            frameBorder="0" 
            height="450" 
            style="width:100%;max-width:660px;overflow:hidden;border-radius:10px;" 
            sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-storage-access-by-user-activation allow-top-navigation-by-user-activation" 
            src="{base_url}">
    </iframe>
    """
    return apple_embed
```

### 2. 🎬 Videos - Osadzanie Video

#### YouTube Embed
```python
def embed_youtube_video(video_id, start_time=0):
    """Osadza video z YouTube"""
    youtube_embed = f"""
    <iframe width="100%" 
            height="400" 
            src="https://www.youtube.com/embed/{video_id}?start={start_time}&rel=0&showinfo=0" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
    </iframe>
    """
    return youtube_embed

# Użycie z timestampem
st.markdown(embed_youtube_video("video_id", start_time=120), unsafe_allow_html=True)
```

#### Vimeo Embed
```python
def embed_vimeo_video(video_id):
    """Osadza video z Vimeo"""
    vimeo_embed = f"""
    <iframe src="https://player.vimeo.com/video/{video_id}?badge=0&autopause=0&player_id=0&app_id=58479" 
            width="100%" 
            height="400" 
            frameborder="0" 
            allow="autoplay; fullscreen; picture-in-picture" 
            allowfullscreen 
            title="Video">
    </iframe>
    """
    return vimeo_embed
```

#### Wistia Embed
```python
def embed_wistia_video(video_id):
    """Osadza video z Wistia (popularne w edukacji)"""
    wistia_embed = f"""
    <iframe src="https://fast.wistia.net/embed/iframe/{video_id}?seo=false" 
            title="Video" 
            allow="autoplay; fullscreen" 
            allowtransparency="true" 
            frameborder="0" 
            scrolling="no" 
            class="wistia_embed" 
            name="wistia_embed" 
            msallowfullscreen 
            width="100%" 
            height="400">
    </iframe>
    """
    return wistia_embed
```

### 3. 📻 Własne Audio Files

#### HTML5 Audio Player
```python
def embed_local_audio(audio_path, title="Audio"):
    """Osadza lokalny plik audio"""
    audio_embed = f"""
    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h4 style="margin-bottom: 15px; color: #333;">🎧 {title}</h4>
        <audio controls style="width: 100%;">
            <source src="{audio_path}" type="audio/mpeg">
            <source src="{audio_path}" type="audio/wav">
            Twoja przeglądarka nie obsługuje odtwarzacza audio.
        </audio>
    </div>
    """
    return audio_embed
```

### 4. 🎥 Własne Video Files

#### HTML5 Video Player
```python
def embed_local_video(video_path, title="Video", poster_path=None):
    """Osadza lokalny plik video"""
    poster_attr = f'poster="{poster_path}"' if poster_path else ''
    
    video_embed = f"""
    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h4 style="margin-bottom: 15px; color: #333;">🎬 {title}</h4>
        <video controls style="width: 100%; border-radius: 8px;" {poster_attr}>
            <source src="{video_path}" type="video/mp4">
            <source src="{video_path}" type="video/webm">
            Twoja przeglądarka nie obsługuje odtwarzacza video.
        </video>
    </div>
    """
    return video_embed
```

## 🔄 Aktualizacja Struktury Tabs

### Nowa Struktura JSON z Osadzonymi Mediami

```json
{
  "learning": {
    "tabs": {
      "📚 Tekst": {
        "sections": [
          {
            "title": "Wprowadzenie do C-IQ",
            "content": "..."
          }
        ]
      },
      "🎧 Podcast": {
        "sections": [
          {
            "title": "Podcast - Conversational Intelligence",
            "content": "EMBED_SPOTIFY:episode_id_here",
            "embed_type": "spotify_podcast",
            "embed_id": "4rAGhD3ALoGvK3E4tBL9vO",
            "description": "Pogłębiona rozmowa o neurobiologii komunikacji"
          }
        ]
      },
      "🎬 Video": {
        "sections": [
          {
            "title": "Video - C-IQ w Praktyce",
            "content": "EMBED_YOUTUBE:zWBujW9o2Hc",
            "embed_type": "youtube",
            "embed_id": "zWBujW9o2Hc",
            "start_time": 0,
            "description": "Praktyczne zastosowanie Conversational Intelligence"
          }
        ]
      }
    }
  }
}
```

### Renderer dla Osadzonych Mediów

```python
# utils/media_embed.py

import streamlit as st
import re

def render_embedded_content(content, section_data=None):
    """Renderuje zawartość z obsługą osadzonych mediów"""
    
    # Sprawdź czy to embed directive
    if content.startswith("EMBED_"):
        return render_embed_directive(content, section_data)
    
    # Sprawdź czy jest embed_type w section_data
    if section_data and section_data.get('embed_type'):
        return render_embed_from_metadata(section_data)
    
    # Standardowa zawartość HTML
    return st.markdown(content, unsafe_allow_html=True)

def render_embed_directive(content, section_data):
    """Renderuje media na podstawie directive w content"""
    
    if content.startswith("EMBED_SPOTIFY:"):
        episode_id = content.replace("EMBED_SPOTIFY:", "")
        st.markdown(embed_spotify_podcast(episode_id), unsafe_allow_html=True)
        
    elif content.startswith("EMBED_YOUTUBE:"):
        video_id = content.replace("EMBED_YOUTUBE:", "")
        start_time = section_data.get('start_time', 0) if section_data else 0
        st.markdown(embed_youtube_video(video_id, start_time), unsafe_allow_html=True)
        
    elif content.startswith("EMBED_SOUNDCLOUD:"):
        track_url = content.replace("EMBED_SOUNDCLOUD:", "")
        st.markdown(embed_soundcloud_audio(track_url), unsafe_allow_html=True)
        
    elif content.startswith("EMBED_LOCAL_AUDIO:"):
        audio_path = content.replace("EMBED_LOCAL_AUDIO:", "")
        title = section_data.get('title', 'Audio') if section_data else 'Audio'
        st.markdown(embed_local_audio(audio_path, title), unsafe_allow_html=True)
        
    elif content.startswith("EMBED_LOCAL_VIDEO:"):
        video_path = content.replace("EMBED_LOCAL_VIDEO:", "")
        title = section_data.get('title', 'Video') if section_data else 'Video'
        poster = section_data.get('poster', None) if section_data else None
        st.markdown(embed_local_video(video_path, title, poster), unsafe_allow_html=True)

def render_embed_from_metadata(section_data):
    """Renderuje media na podstawie metadanych sekcji"""
    
    embed_type = section_data.get('embed_type')
    embed_id = section_data.get('embed_id')
    
    if embed_type == 'spotify_podcast' and embed_id:
        st.markdown(embed_spotify_podcast(embed_id), unsafe_allow_html=True)
        
    elif embed_type == 'youtube' and embed_id:
        start_time = section_data.get('start_time', 0)
        st.markdown(embed_youtube_video(embed_id, start_time), unsafe_allow_html=True)
        
    elif embed_type == 'soundcloud' and embed_id:
        st.markdown(embed_soundcloud_audio(embed_id), unsafe_allow_html=True)
        
    # Dodaj opis jeśli dostępny
    if 'description' in section_data:
        st.markdown(f"*{section_data['description']}*")

# Funkcje embed (jak wcześniej zdefiniowane)
def embed_spotify_podcast(episode_id):
    return f"""
    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <iframe src="https://open.spotify.com/embed/episode/{episode_id}?utm_source=generator" 
                width="100%" 
                height="352" 
                frameBorder="0" 
                allowfullscreen="" 
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                loading="lazy">
        </iframe>
    </div>
    """

def embed_youtube_video(video_id, start_time=0):
    return f"""
    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <iframe width="100%" 
                height="400" 
                src="https://www.youtube.com/embed/{video_id}?start={start_time}&rel=0&showinfo=0" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
        </iframe>
    </div>
    """

def embed_soundcloud_audio(track_url):
    return f"""
    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <iframe width="100%" 
                height="166" 
                scrolling="no" 
                frameborder="no" 
                allow="autoplay" 
                src="https://w.soundcloud.com/player/?url={track_url}&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true">
        </iframe>
    </div>
    """
```

## 🔄 Aktualizacja Lesson Renderer

### Modyfikacja views/lesson.py

```python
# W views/lesson.py - dodaj import
from utils.media_embed import render_embedded_content

# Zmodyfikuj funkcję renderowania sekcji
def render_section(section):
    """Renderuje pojedynczą sekcję z obsługą mediów"""
    if 'title' in section:
        st.subheader(section['title'])
    
    if 'content' in section:
        # Używaj nowego renderera z obsługą mediów
        render_embedded_content(section['content'], section)
    
    # Dodaj separator między sekcjami
    st.markdown("---")
```

## 📋 Implementacja dla Lekcji 11

### Krok 1: Aktualizuj JSON Lekcji

```json
{
  "sections": {
    "learning": {
      "tabs": [
        {
          "name": "📚 Tekst",
          "sections": [
            // istniejące sekcje tekstowe
          ]
        },
        {
          "name": "🎧 Podcast", 
          "sections": [
            {
              "title": "Podcast - Wprowadzenie do Conversational Intelligence",
              "content": "EMBED_YOUTUBE:1eram4uEQ58",
              "embed_type": "youtube",
              "embed_id": "1eram4uEQ58",
              "description": "Podsumowanie kluczowych koncepcji z książki Judith Glaser w formacie audio"
            }
          ]
        },
        {
          "name": "🎬 Video",
          "sections": [
            {
              "title": "Video - Inteligencja konwersacyjna w pigułce", 
              "content": "EMBED_YOUTUBE:zWBujW9o2Hc",
              "embed_type": "youtube",
              "embed_id": "zWBujW9o2Hc",
              "description": "Dynamiczna prezentacja teorii i praktyki C-IQ w 10 minut"
            }
          ]
        }
      ]
    }
  }
}
```

### Krok 2: Utwórz Narzędzia Media

```bash
# Utwórz katalog dla mediów
mkdir -p static/media/audio
mkdir -p static/media/video

# Utwórz moduł obsługi mediów
touch utils/media_embed.py
```

### Krok 3: Test Implementacji

```python
# test_media_embed.py
import streamlit as st
from utils.media_embed import embed_youtube_video, embed_spotify_podcast

st.title("Test Osadzonych Mediów")

# Test YouTube
st.subheader("🎬 Test YouTube")
st.markdown(embed_youtube_video("zWBujW9o2Hc"), unsafe_allow_html=True)

# Test Spotify (potrzebny rzeczywisty episode_id)
st.subheader("🎧 Test Spotify")
# st.markdown(embed_spotify_podcast("episode_id"), unsafe_allow_html=True)
```

## 🎯 Korzyści Rozwiązania

### ✅ Zalety
- **Lepsze UX** - użytkownik nie opuszcza aplikacji
- **Kontekst** - zachowanie ciągłości nauki
- **Kontrola** - możliwość dostosowania odtwarzacza
- **Analytics** - śledzenie interakcji z mediami
- **Offline** - możliwość hostowania własnych plików

### 📊 Metryki Sukcesu
- Zwiększony czas spędzony w aplikacji
- Wyższa kompletność lekcji
- Lepsza ocena UX od użytkowników
- Mniej bounces na zewnętrzne strony

## 🚀 Następne Kroki

1. **Implementuj utils/media_embed.py**
2. **Aktualizuj strukturę JSON lekcji 11**
3. **Zmodyfikuj lesson renderer**
4. **Przetestuj z rzeczywistymi mediami**
5. **Rozszerz na inne lekcje**

---

📝 **Uwaga**: Pamiętaj o sprawdzeniu polityki embeddingu platform (szczególnie Spotify) oraz o responsive design dla urządzeń mobilnych.
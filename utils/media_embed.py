"""
Moduł do obsługi osadzonych mediów w aplikacji Streamlit
Obsługuje: YouTube, Spotify, SoundCloud, Apple Podcasts, lokalne pliki
"""

import streamlit as st
import re
from urllib.parse import quote


def render_embedded_content(content, section_data=None):
    """Renderuje zawartość z obsługą osadzonych mediów"""
    
    # Sprawdź czy to embed directive
    if isinstance(content, str) and content.startswith("EMBED_"):
        return render_embed_directive(content, section_data)
    
    # Sprawdź czy jest embed_type w section_data
    if section_data and section_data.get('embed_type'):
        return render_embed_from_metadata(section_data)
    
    # Standardowa zawartość HTML
    if isinstance(content, str):
        st.markdown(content, unsafe_allow_html=True)
    

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
        
    # Dodaj opis jeśli dostępny
    if section_data and 'description' in section_data:
        st.markdown(f"*{section_data['description']}*")


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
        
    elif embed_type == 'apple_podcast' and embed_id:
        episode_id = section_data.get('episode_id')
        st.markdown(embed_apple_podcast(embed_id, episode_id), unsafe_allow_html=True)
        
    # Dodaj opis jeśli dostępny
    if 'description' in section_data:
        st.markdown(f"*{section_data['description']}*")


# ===== SPOTIFY EMBEDS =====

def embed_spotify_podcast(episode_id):
    """Osadza podcast ze Spotify"""
    return f"""
    <div style="background: linear-gradient(135deg, #1db954 0%, #1ed760 100%); padding: 25px; border-radius: 15px; margin: 20px 0;">
        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 15px;">
                <h4 style="color: #1db954; margin: 0; font-size: 1.2rem;">🎧 Spotify Podcast</h4>
            </div>
            <iframe src="https://open.spotify.com/embed/episode/{episode_id}?utm_source=generator" 
                    width="100%" 
                    height="352" 
                    frameBorder="0" 
                    allowfullscreen="" 
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                    loading="lazy"
                    style="border-radius: 8px;">
            </iframe>
        </div>
    </div>
    """

def embed_spotify_track(track_id):
    """Osadza utwór ze Spotify"""
    return f"""
    <div style="background: linear-gradient(135deg, #1db954 0%, #1ed760 100%); padding: 25px; border-radius: 15px; margin: 20px 0;">
        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 15px;">
                <h4 style="color: #1db954; margin: 0; font-size: 1.2rem;">🎵 Spotify Music</h4>
            </div>
            <iframe src="https://open.spotify.com/embed/track/{track_id}?utm_source=generator" 
                    width="100%" 
                    height="352" 
                    frameBorder="0" 
                    allowfullscreen="" 
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                    loading="lazy"
                    style="border-radius: 8px;">
            </iframe>
        </div>
    </div>
    """


# ===== YOUTUBE EMBEDS =====

def embed_youtube_video(video_id, start_time=0, title=None):
    """Osadza video z YouTube"""
    title_html = f"<h4 style='color: #ff0000; margin: 0 0 15px 0; font-size: 1.2rem;'>🎬 {title}</h4>" if title else "<h4 style='color: #ff0000; margin: 0 0 15px 0; font-size: 1.2rem;'>🎬 YouTube Video</h4>"
    
    return f"""
    <div style="background: linear-gradient(135deg, #ff0000 0%, #ff4444 100%); padding: 25px; border-radius: 15px; margin: 20px 0;">
        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 15px;">
                {title_html}
            </div>
            <div style="position: relative; width: 100%; height: 0; padding-bottom: 56.25%;">
                <iframe src="https://www.youtube.com/embed/{video_id}?start={start_time}&rel=0&showinfo=0&modestbranding=1" 
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 8px;"
                        frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                </iframe>
            </div>
        </div>
    </div>
    """

def embed_youtube_playlist(playlist_id, title=None):
    """Osadza playlistę z YouTube"""
    title_html = f"<h4 style='color: #ff0000; margin: 0 0 15px 0; font-size: 1.2rem;'>🎬 {title}</h4>" if title else "<h4 style='color: #ff0000; margin: 0 0 15px 0; font-size: 1.2rem;'>🎬 YouTube Playlist</h4>"
    
    return f"""
    <div style="background: linear-gradient(135deg, #ff0000 0%, #ff4444 100%); padding: 25px; border-radius: 15px; margin: 20px 0;">
        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 15px;">
                {title_html}
            </div>
            <div style="position: relative; width: 100%; height: 0; padding-bottom: 56.25%;">
                <iframe src="https://www.youtube.com/embed/videoseries?list={playlist_id}&rel=0&showinfo=0" 
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 8px;"
                        frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                </iframe>
            </div>
        </div>
    </div>
    """


# ===== SOUNDCLOUD EMBEDS =====

def embed_soundcloud_audio(track_url, title=None):
    """Osadza audio z SoundCloud"""
    encoded_url = quote(track_url, safe='')
    title_html = f"<h4 style='color: #ff6b35; margin: 0 0 15px 0; font-size: 1.2rem;'>🎧 {title}</h4>" if title else "<h4 style='color: #ff6b35; margin: 0 0 15px 0; font-size: 1.2rem;'>🎧 SoundCloud Audio</h4>"
    
    return f"""
    <div style="background: linear-gradient(135deg, #ff6b35 0%, #ff8a50 100%); padding: 25px; border-radius: 15px; margin: 20px 0;">
        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 15px;">
                {title_html}
            </div>
            <iframe width="100%" 
                    height="166" 
                    scrolling="no" 
                    frameborder="no" 
                    allow="autoplay" 
                    src="https://w.soundcloud.com/player/?url={encoded_url}&color=%23ff6b35&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"
                    style="border-radius: 8px;">
            </iframe>
        </div>
    </div>
    """


# ===== APPLE PODCASTS EMBEDS =====

def embed_apple_podcast(podcast_id, episode_id=None, title=None):
    """Osadza podcast z Apple Podcasts"""
    base_url = f"https://embed.podcasts.apple.com/us/podcast/id{podcast_id}"
    if episode_id:
        base_url += f"?i={episode_id}"
    
    title_html = f"<h4 style='color: #9146ff; margin: 0 0 15px 0; font-size: 1.2rem;'>🎙️ {title}</h4>" if title else "<h4 style='color: #9146ff; margin: 0 0 15px 0; font-size: 1.2rem;'>🎙️ Apple Podcasts</h4>"
    
    return f"""
    <div style="background: linear-gradient(135deg, #9146ff 0%, #a855f7 100%); padding: 25px; border-radius: 15px; margin: 20px 0;">
        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 15px;">
                {title_html}
            </div>
            <iframe allow="autoplay *; encrypted-media *; fullscreen *; clipboard-write" 
                    frameBorder="0" 
                    height="450" 
                    style="width:100%;max-width:660px;overflow:hidden;border-radius:8px;" 
                    sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-storage-access-by-user-activation allow-top-navigation-by-user-activation" 
                    src="{base_url}">
            </iframe>
        </div>
    </div>
    """


# ===== VIMEO EMBEDS =====

def embed_vimeo_video(video_id, title=None):
    """Osadza video z Vimeo"""
    title_html = f"<h4 style='color: #1ab7ea; margin: 0 0 15px 0; font-size: 1.2rem;'>🎬 {title}</h4>" if title else "<h4 style='color: #1ab7ea; margin: 0 0 15px 0; font-size: 1.2rem;'>🎬 Vimeo Video</h4>"
    
    return f"""
    <div style="background: linear-gradient(135deg, #1ab7ea 0%, #1fc7ea 100%); padding: 25px; border-radius: 15px; margin: 20px 0;">
        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 15px;">
                {title_html}
            </div>
            <div style="position: relative; width: 100%; height: 0; padding-bottom: 56.25%;">
                <iframe src="https://player.vimeo.com/video/{video_id}?badge=0&autopause=0&player_id=0&app_id=58479" 
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 8px;"
                        frameborder="0" 
                        allow="autoplay; fullscreen; picture-in-picture" 
                        allowfullscreen 
                        title="Video">
                </iframe>
            </div>
        </div>
    </div>
    """


# ===== LOKALNE PLIKI =====

def embed_local_audio(audio_path, title="Audio"):
    """Osadza lokalny plik audio"""
    return f"""
    <div style="background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%); padding: 25px; border-radius: 15px; margin: 20px 0;">
        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 15px;">
                <h4 style="color: #4caf50; margin: 0; font-size: 1.2rem;">🎧 {title}</h4>
            </div>
            <audio controls style="width: 100%; border-radius: 8px;">
                <source src="{audio_path}" type="audio/mpeg">
                <source src="{audio_path}" type="audio/wav">
                <source src="{audio_path}" type="audio/ogg">
                Twoja przeglądarka nie obsługuje odtwarzacza audio.
            </audio>
        </div>
    </div>
    """

def embed_local_video(video_path, title="Video", poster_path=None):
    """Osadza lokalny plik video"""
    poster_attr = f'poster="{poster_path}"' if poster_path else ''
    
    return f"""
    <div style="background: linear-gradient(135deg, #2196f3 0%, #42a5f5 100%); padding: 25px; border-radius: 15px; margin: 20px 0;">
        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 15px;">
                <h4 style="color: #2196f3; margin: 0; font-size: 1.2rem;">🎬 {title}</h4>
            </div>
            <video controls style="width: 100%; border-radius: 8px;" {poster_attr}>
                <source src="{video_path}" type="video/mp4">
                <source src="{video_path}" type="video/webm">
                <source src="{video_path}" type="video/ogg">
                Twoja przeglądarka nie obsługuje odtwarzacza video.
            </video>
        </div>
    </div>
    """


# ===== HELPER FUNCTIONS =====

def extract_youtube_id(url):
    """Wyciąga ID video z URL YouTube"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def extract_vimeo_id(url):
    """Wyciąga ID video z URL Vimeo"""
    pattern = r'vimeo\.com\/(\d+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def extract_spotify_id(url):
    """Wyciąga ID z URL Spotify"""
    pattern = r'spotify\.com\/(episode|track|playlist)\/([^?]+)'
    match = re.search(pattern, url)
    return match.group(2) if match else None


# ===== TEST FUNCTIONS =====

def test_embeds():
    """Funkcja testowa dla wszystkich typów embeds"""
    st.title("🎥🎧 Test Osadzonych Mediów")
    
    st.subheader("🎬 YouTube Video")
    st.markdown(embed_youtube_video("zWBujW9o2Hc", title="Conversational Intelligence"), unsafe_allow_html=True)
    
    st.subheader("🎧 SoundCloud Audio")
    st.markdown(embed_soundcloud_audio("https://soundcloud.com/user/track", title="Test Audio"), unsafe_allow_html=True)
    
    st.subheader("🎵 Spotify Track")
    st.markdown(embed_spotify_track("4uLU6hMCjMI75M1A2tKUQC"), unsafe_allow_html=True)
    
    st.subheader("🎙️ Apple Podcast")
    st.markdown(embed_apple_podcast("1535844815", title="Test Podcast"), unsafe_allow_html=True)


if __name__ == "__main__":
    # Uruchom testy jeśli plik jest wywołany bezpośrednio
    test_embeds()
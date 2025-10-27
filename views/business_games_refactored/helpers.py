"""
Funkcje pomocnicze dla Business Games
Zawiera utility functions używane w całym module
"""

from typing import Dict
import streamlit as st


def get_contract_reward_coins(contract: Dict) -> int:
    """Bezpieczne pobranie nagród w monetach z kontraktu (obsługa starych i nowych formatów)"""
    reward_data = contract.get("reward", 0)
    if isinstance(reward_data, dict):
        return reward_data.get("coins", 0)
    return reward_data  # Stary format - reward jako int


def get_contract_reward_reputation(contract: Dict) -> int:
    """Bezpieczne pobranie nagród w reputacji z kontraktu"""
    reward_data = contract.get("reward", 0)
    if isinstance(reward_data, dict):
        return reward_data.get("reputation", 0)
    return 0  # Stary format nie miał reputacji w reward


def get_game_data(user_data, industry_id="consulting"):
    """Pobiera dane gry dla wybranej branży (z backward compatibility)"""
    # Najpierw spróbuj nowej struktury
    if "business_games" in user_data and industry_id in user_data["business_games"]:
        return user_data["business_games"][industry_id]
    # Fallback na starą strukturę (backward compatibility)
    elif "business_game" in user_data:
        return user_data["business_game"]
    # Jeśli nic nie znaleziono - zwróć pustą strukturę (nie None!)
    return {}


def save_game_data(user_data, bg_data, industry_id="consulting"):
    """Zapisuje dane gry dla wybranej branży (z backward compatibility)"""
    # Zapisz w nowej strukturze
    if "business_games" not in user_data:
        user_data["business_games"] = {}
    user_data["business_games"][industry_id] = bg_data
    # Dla backward compatibility - zapisz też w starej strukturze jeśli istnieje
    if "business_game" in user_data and industry_id == "consulting":
        user_data["business_game"] = bg_data
    return user_data


def play_coin_sound():
    """Odtwarza dźwięk brzęczących monet przy nagrodzie"""
    # Prosty dźwięk za pomocą HTML audio z CDN
    # Użyj darmowego dźwięku monet z freesound.org lub podobnego
    st.markdown(
        """
        <audio autoplay>
            <source src="https://assets.mixkit.co/active_storage/sfx/2003/2003-preview.mp3" type="audio/mpeg">
        </audio>
        """,
        unsafe_allow_html=True
    )

"""
Skrypt do dodania fikcyjnych danych historii rankingu dla testów
"""

import json
from datetime import datetime, timedelta
from data.users_new import load_user_data, save_single_user

def add_fake_ranking_history():
    """Dodaje fikcyjne dane historyczne dla 8 graczy za ostatnie 3 dni"""
    
    # Wczytaj wszystkich użytkowników
    all_users = load_user_data()
    
    # Znajdź graczy z business_game
    players_with_game = [(username, data) for username, data in all_users.items() 
                         if data.get("business_game")]
    
    if len(players_with_game) < 8:
        print(f"❌ Znaleziono tylko {len(players_with_game)} graczy z business_game. Potrzeba co najmniej 8.")
        print(f"   Dostępni gracze: {[u for u, _ in players_with_game]}")
        return
    
    # Wybierz pierwszych 8 graczy
    test_players = players_with_game[:8]
    
    print(f"📊 Dodawanie fikcyjnych danych dla graczy:")
    for username, _ in test_players:
        print(f"  - {username}")
    
    # Generuj dane za ostatnie 3 dni
    today = datetime.now()
    
    # Scenariusze pozycji dla każdego gracza (3 dni wstecz)
    # Gracz 1: Awans z 3 na 1 (brąz -> złoto)
    player1_positions = [3, 2, 1]
    player1_scores = [850, 1050, 1250]
    
    # Gracz 2: Spadek z 1 na 2 (złoto -> srebro)
    player2_positions = [1, 2, 2]
    player2_scores = [1200, 1100, 1150]
    
    # Gracz 3: Stabilna pozycja 3 (brąz)
    player3_positions = [4, 3, 3]
    player3_scores = [800, 900, 950]
    
    # Gracz 4: Stabilna pozycja 4 (TOP 10, szary)
    player4_positions = [5, 4, 4]
    player4_scores = [700, 750, 780]
    
    # Gracz 5: Awans z 7 na 5 (TOP 10, szary)
    player5_positions = [7, 6, 5]
    player5_scores = [600, 680, 720]
    
    # Gracz 6: Spadek z 5 na 6 (TOP 10, szary)
    player6_positions = [5, 6, 6]
    player6_scores = [710, 690, 700]
    
    # Gracz 7: Stabilna pozycja 7 (TOP 10, szary)
    player7_positions = [8, 7, 7]
    player7_scores = [580, 620, 650]
    
    # Gracz 8: Awans z 10 na 8 (TOP 10, szary)
    player8_positions = [10, 9, 8]
    player8_scores = [500, 550, 600]
    
    positions_data = [
        player1_positions, player2_positions, player3_positions, player4_positions,
        player5_positions, player6_positions, player7_positions, player8_positions
    ]
    scores_data = [
        player1_scores, player2_scores, player3_scores, player4_scores,
        player5_scores, player6_scores, player7_scores, player8_scores
    ]
    
    # Dodaj dane dla każdego gracza
    for idx, (username, user_data) in enumerate(test_players):
        bg_data = user_data["business_game"]
        
        # Inicjalizuj position_history jeśli nie istnieje
        if "position_history" not in bg_data.get("ranking", {}):
            if "ranking" not in bg_data:
                bg_data["ranking"] = {}
            bg_data["ranking"]["position_history"] = []
        
        history = bg_data["ranking"]["position_history"]
        
        # Wyczyść stare dane testowe (opcjonalnie)
        # history.clear()
        
        # Dodaj wpisy za ostatnie 3 dni
        for day_offset in range(3):
            date = today - timedelta(days=2-day_offset)  # 2 dni temu, wczoraj, dziś
            
            # Dodaj dla różnych typów rankingów z różnymi pozycjami
            # Overall - bazowe pozycje
            history.append({
                "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                "type": "overall",
                "position": positions_data[idx][day_offset],
                "score": scores_data[idx][day_offset]
            })
            
            # Revenue - pozycje +1 (nieco gorsze)
            history.append({
                "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                "type": "revenue",
                "position": min(positions_data[idx][day_offset] + 1, 15),  # Max 15
                "score": int(scores_data[idx][day_offset] * 0.9)
            })
            
            # Quality - pozycje -1 (nieco lepsze) lub bez zmiany jeśli na 1
            history.append({
                "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                "type": "quality",
                "position": max(positions_data[idx][day_offset] - 1, 1),  # Min 1
                "score": int(scores_data[idx][day_offset] * 1.1)
            })
            
            # Productivity - pozycje +2 (jeszcze gorsze)
            history.append({
                "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                "type": "productivity_30d",
                "position": min(positions_data[idx][day_offset] + 2, 20),  # Max 20
                "score": int(scores_data[idx][day_offset] * 0.8)
            })
        
        # Zapisz zaktualizowane dane
        save_single_user(username, user_data)
        
        print(f"✅ {username}: Dodano dane za ostatnie 3 dni")
        print(f"   Pozycje: {positions_data[idx]}")
        print(f"   Scores: {scores_data[idx]}")
    
    print("\n🎉 Gotowe! Odśwież stronę Business Games aby zobaczyć wykresy.")
    print("💡 Sprawdź różne typy rankingów - dane zostały dodane dla wszystkich.")

if __name__ == "__main__":
    add_fake_ranking_history()

"""
Test Heinz Cleanup Logic
Sprawdza czy nowy gracz ma czysty stan bez demo data
"""

from utils.business_game import initialize_fmcg_game_new
from utils.reputation_system import calculate_overall_rating, get_client_weight

def test_heinz_cleanup():
    """Test czy cleanup działa poprawnie"""
    
    print("="*80)
    print("TEST HEINZ CLEANUP - Nowy gracz powinien mieć 0 client points")
    print("="*80)
    
    # Initialize new game
    game_data = initialize_fmcg_game_new(username="test_cleanup", scenario="heinz_food_service")
    
    # Get clients from fmcg_state (not top-level)
    fmcg_state = game_data.get("fmcg_state", {})
    clients = fmcg_state.get("clients", {})
    game_state = fmcg_state  # Use fmcg_state as game_state for calculations
    
    print(f"\n📊 Załadowano {len(clients)} klientów Heinz")
    
    # Check each client
    issues = []
    for client_id, client in clients.items():
        status = client.get("status", "NO_STATUS")
        convinced = client.get("convinced_products", {})
        conviction_data = client.get("conviction_data", {})
        relationship_score = client.get("relationship_score", 0)
        reputation = client.get("reputation", 0)
        visits = client.get("visits_count", 0)
        
        # Check for issues
        if status != "PROSPECT_NOT_CONTACTED":
            issues.append(f"❌ {client_id}: status={status} (powinno być PROSPECT_NOT_CONTACTED)")
        
        if convinced:
            issues.append(f"❌ {client_id}: convinced_products={len(convinced)} (powinno być puste)")
        
        if conviction_data:
            issues.append(f"❌ {client_id}: conviction_data={len(conviction_data)} produktów (powinno być puste)")
        
        if relationship_score != 50:
            issues.append(f"❌ {client_id}: relationship_score={relationship_score} (powinno być 50)")
        
        if reputation != 50:
            issues.append(f"❌ {client_id}: reputation={reputation} (powinno być 50)")
        
        if visits != 0:
            issues.append(f"❌ {client_id}: visits_count={visits} (powinno być 0)")
    
    # Calculate reputation
    print("\n📈 Obliczam Client Points...")
    
    total_client_points = 0
    for client_id, client in clients.items():
        weight = get_client_weight(client)
        rep = client.get("reputation", 50)
        points = rep * weight
        
        if weight > 0:
            print(f"  {client_id}: rep={rep} × weight={weight} = {points:.1f} pts")
            total_client_points += points
    
    print(f"\n✨ Total Client Points: {total_client_points:.1f} pts")
    
    # Calculate overall rating
    overall_points = calculate_overall_rating(game_state, clients)
    
    print(f"🎯 Overall Rating: {overall_points:.1f} pts")
    
    # Expected: Company Points only (professionalism=100 × 0.30 × 0.5 = 15)
    expected_company = 15.0  # Changed from 30.0
    expected_client = 0.0
    expected_total = expected_company + expected_client
    
    print(f"\n📊 OCZEKIWANE WARTOŚCI:")
    print(f"   Company Points: {expected_company:.1f} pts (professionalism=100 × 0.30 × 0.5)")
    print(f"   Client Points: {expected_client:.1f} pts (wszyscy PROSPECT_NOT_CONTACTED)")
    print(f"   Total: {expected_total:.1f} pts")
    
    # Report issues
    print("\n" + "="*80)
    if issues:
        print("❌ ZNALEZIONO PROBLEMY:")
        for issue in issues:
            print(f"   {issue}")
        print(f"\n   SUMA: {len(issues)} problemów")
    else:
        print("✅ CLEANUP DZIAŁA POPRAWNIE!")
        print("   - Wszyscy klienci: PROSPECT_NOT_CONTACTED")
        print("   - Reputation: 50/100")
        print("   - Relationship: 50/100")
        print("   - Wizyty: 0")
        print("   - Convinced products: puste")
        print("   - Conviction data: puste")
    
    print("="*80)
    
    # Check if overall points match expected
    if abs(overall_points - expected_total) < 0.1:
        print(f"✅ Overall Rating poprawny: {overall_points:.1f} pts")
    else:
        print(f"❌ Overall Rating niepoprawny: {overall_points:.1f} pts (oczekiwano {expected_total:.1f})")
    
    return len(issues) == 0


if __name__ == "__main__":
    success = test_heinz_cleanup()
    exit(0 if success else 1)

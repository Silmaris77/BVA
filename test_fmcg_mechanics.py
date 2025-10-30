"""
Test FMCG Core Mechanics
Testuje: wizyty, reputację, statusy klientów, energię
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.fmcg_mechanics import (
    convert_prospect_to_active,
    lose_client,
    check_client_status_changes,
    calculate_reputation_change,
    apply_reputation_decay,
    update_client_reputation,
    calculate_visit_energy_cost,
    calculate_travel_time,
    execute_visit_placeholder,
    advance_day,
    get_client_status_summary,
    get_clients_needing_visit
)
from data.industries.fmcg_data_schema import create_new_client, initialize_fmcg_game_state


def test_client_status_transitions():
    """Test transitions: PROSPECT → ACTIVE → LOST"""
    print("\n🧪 TEST 1: Client Status Transitions")
    print("=" * 60)
    
    # Create test client (PROSPECT)
    client = create_new_client(
        client_id="test_001",
        name="Test Sklep",
        client_type="Sklep osiedlowy",
        segment="traditional_trade",
        location="Warszawa, Test",
        lat=52.08,
        lon=21.02,
        distance=1.5,
        owner_name="Jan Testowy",
        potential=3000
    )
    
    print(f"✓ Created client: {client['name']}")
    print(f"  Status: {client['status']}")
    print(f"  Reputation: {client.get('reputation', 'N/A')}")
    
    # PROSPECT → ACTIVE
    print(f"\n📈 Converting PROSPECT → ACTIVE (first order: 2500 PLN)...")
    client = convert_prospect_to_active(client, first_order_value=2500)
    
    print(f"  ✅ Status: {client['status']}")
    print(f"  Reputation: {client['reputation']}")
    print(f"  Monthly value: {client['monthly_value']} PLN")
    print(f"  Total sales: {client['total_sales']} PLN")
    
    assert client["status"] == "ACTIVE", "Should be ACTIVE"
    assert client["reputation"] == 50, "Should start with 50 reputation"
    
    # ACTIVE → LOST
    print(f"\n📉 Losing client (reason: no_visits)...")
    client = lose_client(client, reason="no_visits")
    
    print(f"  ❌ Status: {client['status']}")
    print(f"  Lost reason: {client['lost_reason']}")
    print(f"  Win-back difficulty: {client['win_back_difficulty']}/5")
    
    assert client["status"] == "LOST", "Should be LOST"
    assert client["lost_reason"] == "no_visits", "Should have correct reason"
    
    print("\n✅ Status transitions: PASSED")


def test_reputation_system():
    """Test reputation calculations"""
    print("\n🧪 TEST 2: Reputation System")
    print("=" * 60)
    
    # Test different visit qualities
    test_cases = [
        (5, 0, 0, True, [], "5⭐ + order"),
        (4, 2, 0, False, [], "4⭐ + 2 tasks"),
        (3, 0, 0, False, [], "3⭐ neutral"),
        (2, 0, 1, False, [], "2⭐ + failed task"),
        (1, 0, 0, False, [], "1⭐ terrible"),
        (4, 0, 0, True, ["gratis", "rabat"], "4⭐ + tools"),
    ]
    
    for quality, tasks_done, tasks_fail, order, tools, description in test_cases:
        change = calculate_reputation_change(
            visit_quality=quality,
            tasks_completed=tasks_done,
            tasks_failed=tasks_fail,
            order_placed=order,
            tools_used=tools
        )
        print(f"  {description:25} → {change:+3d} reputation")
    
    # Test reputation decay
    print(f"\n📉 Reputation decay test:")
    client = create_new_client(
        client_id="test_002",
        name="Test Sklep 2",
        client_type="Sklep",
        segment="traditional_trade",
        location="Test",
        lat=52.08,
        lon=21.02,
        distance=1.0,
        owner_name="Test",
        potential=2000
    )
    client = convert_prospect_to_active(client, 2000)
    client["reputation"] = 80
    client["visit_frequency_required"] = 14
    
    decay_tests = [
        (10, "10 days (within frequency)"),
        (14, "14 days (exactly on time)"),
        (17, "17 days (3 days late)"),
        (20, "20 days (6 days late)"),
        (30, "30 days (16 days late)"),
    ]
    
    for days, description in decay_tests:
        decay = apply_reputation_decay(client, days)
        print(f"  {description:30} → {decay:+3d} decay")
    
    print("\n✅ Reputation system: PASSED")


def test_visit_execution():
    """Test visit execution with energy consumption"""
    print("\n🧪 TEST 3: Visit Execution")
    print("=" * 60)
    
    # Setup
    game_state = initialize_fmcg_game_state()
    client = create_new_client(
        client_id="test_003",
        name="Sklep Test",
        client_type="Sklep osiedlowy",
        segment="traditional_trade",
        location="Test Location",
        lat=52.08,
        lon=21.02,
        distance=5.0,  # 5 km away
        owner_name="Pan Test",
        potential=3500
    )
    
    print(f"Initial state:")
    print(f"  Energy: {game_state['energy']}%")
    print(f"  Client status: {client['status']}")
    print(f"  Client distance: {client['distance_from_base']} km")
    
    # Calculate costs
    travel_time = calculate_travel_time(client['distance_from_base'])
    energy_cost = calculate_visit_energy_cost(client['distance_from_base'], 45)
    
    print(f"\nVisit costs:")
    print(f"  Travel time: {travel_time} min (one way)")
    print(f"  Energy cost: {energy_cost}%")
    
    # Execute visit (PROSPECT first contact)
    print(f"\n📍 Executing first visit (PROSPECT)...")
    client, game_state, visit_record = execute_visit_placeholder(
        client=client,
        game_state=game_state,
        conversation_quality=4,  # Good conversation
        order_value=0,  # No order yet (first contact)
        tasks_completed=0
    )
    
    print(f"  Status after visit: {client['status']}")
    print(f"  Visits count: {client['visits_count']}")
    print(f"  First contact date: {client.get('first_contact_date', 'N/A')[:10]}")
    print(f"  Energy remaining: {game_state['energy']}%")
    
    assert client["status"] == "PROSPECT", "Should still be PROSPECT (no order)"
    assert client["visits_count"] == 1, "Should have 1 visit"
    assert client["first_contact_date"] is not None, "Should have first contact date"
    
    # Second visit with order → ACTIVE
    print(f"\n📍 Executing second visit with order (PROSPECT → ACTIVE)...")
    client, game_state, visit_record = execute_visit_placeholder(
        client=client,
        game_state=game_state,
        conversation_quality=5,  # Excellent!
        order_value=2800,  # First order!
        tasks_completed=1
    )
    
    print(f"  ✅ Status after visit: {client['status']}")
    print(f"  Reputation: {client['reputation']}")
    print(f"  Total sales: {client['total_sales']} PLN")
    print(f"  Monthly sales (game): {game_state['monthly_sales']} PLN")
    print(f"  Energy remaining: {game_state['energy']}%")
    print(f"  Visits this week: {game_state['visits_this_week']}")
    
    assert client["status"] == "ACTIVE", "Should be ACTIVE after first order"
    assert client["total_sales"] == 2800, "Should have correct sales"
    assert game_state["clients_active"] == 1, "Should have 1 active client"
    
    print("\n✅ Visit execution: PASSED")


def test_day_advancement():
    """Test day advancement and reputation decay"""
    print("\n🧪 TEST 4: Day Advancement")
    print("=" * 60)
    
    # Setup
    game_state = initialize_fmcg_game_state()
    game_state["current_day"] = "Monday"
    game_state["current_week"] = 1
    game_state["energy"] = 30  # Depleted
    
    # Create active client with old last visit
    client = create_new_client(
        client_id="test_004",
        name="Zaniedbany Sklep",
        client_type="Sklep",
        segment="traditional_trade",
        location="Test",
        lat=52.08,
        lon=21.02,
        distance=2.0,
        owner_name="Test",
        potential=2500
    )
    client = convert_prospect_to_active(client, 2000)
    client["reputation"] = 70
    client["visit_frequency_required"] = 14
    # Set last visit 20 days ago
    old_date = datetime.now() - timedelta(days=20)
    client["last_visit_date"] = old_date.isoformat()
    
    clients = {"test_004": client}
    
    print(f"Before advancement:")
    print(f"  Day: {game_state['current_day']}")
    print(f"  Week: {game_state['current_week']}")
    print(f"  Energy: {game_state['energy']}%")
    print(f"  Client reputation: {client['reputation']}")
    print(f"  Days since last visit: 20")
    
    # Advance day
    game_state, clients = advance_day(game_state, clients)
    client = clients["test_004"]
    
    print(f"\nAfter advancement:")
    print(f"  Day: {game_state['current_day']}")
    print(f"  Energy: {game_state['energy']}% (regenerated)")
    print(f"  Client reputation: {client['reputation']} (after decay)")
    print(f"  Client status: {client['status']}")
    
    assert game_state["current_day"] == "Tuesday", "Should advance to Tuesday"
    assert game_state["energy"] == 100, "Should regenerate energy"
    assert client["reputation"] < 70, "Reputation should decay"
    
    # Advance through week
    print(f"\n⏩ Advancing through the week...")
    for i in range(3):  # Tue → Fri (3 more days)
        game_state, clients = advance_day(game_state, clients)
    
    print(f"  Day after 3 more days: {game_state['current_day']}")
    assert game_state["current_day"] == "Friday", "Should be Friday"
    
    # Advance to Monday (new week)
    game_state["visits_this_week"] = 5
    game_state, clients = advance_day(game_state, clients)
    
    print(f"  Day after one more: {game_state['current_day']}")
    print(f"  Week: {game_state['current_week']}")
    print(f"  Visits this week: {game_state['visits_this_week']} (reset)")
    
    assert game_state["current_day"] == "Monday", "Should be Monday"
    assert game_state["current_week"] == 2, "Should be week 2"
    assert game_state["visits_this_week"] == 0, "Should reset visits"
    
    print("\n✅ Day advancement: PASSED")


def test_helper_functions():
    """Test helper functions"""
    print("\n🧪 TEST 5: Helper Functions")
    print("=" * 60)
    
    # Create test clients
    clients = {}
    for i in range(5):
        client = create_new_client(
            client_id=f"test_{i:03d}",
            name=f"Sklep {i}",
            client_type="Sklep",
            segment="traditional_trade",
            location=f"Location {i}",
            lat=52.08,
            lon=21.02,
            distance=float(i),
            owner_name=f"Owner {i}",
            potential=2000
        )
        
        # Mix of statuses
        if i < 2:
            client = convert_prospect_to_active(client, 2000)
        elif i == 4:
            client = convert_prospect_to_active(client, 2000)
            client = lose_client(client, "no_visits")
        
        # Set old visit dates for some
        if i == 0:
            old_date = datetime.now() - timedelta(days=12)
            client["last_visit_date"] = old_date.isoformat()
        
        clients[client["client_id"]] = client
    
    # Test status summary
    summary = get_client_status_summary(clients)
    print(f"Client status summary:")
    for status, count in summary.items():
        print(f"  {status}: {count}")
    
    assert summary["PROSPECT"] == 2, "Should have 2 prospects"
    assert summary["ACTIVE"] == 2, "Should have 2 active"
    assert summary["LOST"] == 1, "Should have 1 lost"
    
    # Test urgent visits
    urgent = get_clients_needing_visit(clients, urgent_threshold_days=5)
    print(f"\nClients needing urgent visit: {len(urgent)}")
    for client_id in urgent:
        print(f"  - {clients[client_id]['name']}")
    
    print("\n✅ Helper functions: PASSED")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🧪 FMCG CORE MECHANICS - TEST SUITE")
    print("=" * 60)
    
    try:
        test_client_status_transitions()
        test_reputation_system()
        test_visit_execution()
        test_day_advancement()
        test_helper_functions()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED:")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

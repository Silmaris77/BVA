"""
FMCG Product Handler - Tasks System
Phase 1: Weekly Tasks (MVP)

Task definitions for different scenarios and weeks.
Auto-assigned on Mondays, deadline Fridays.
"""

from datetime import datetime, timedelta


def get_weekly_tasks(scenario_id, current_week, game_state=None):
    """
    Get tasks for current week based on scenario and week number.
    
    Args:
        scenario_id: Scenario identifier (quick_start, heinz_food_service, lifetime)
        current_week: Current week number (1-8)
        game_state: Current game state dict (for dynamic task generation)
    
    Returns:
        List of task dictionaries
    """
    
    # Week 1 has only onboarding tasks (already implemented)
    if current_week == 1:
        return []  # Onboarding handles Week 1
    
    # Get scenario-specific tasks
    if "heinz" in scenario_id.lower():
        return get_heinz_tasks(current_week, game_state)
    else:
        return get_standard_tasks(current_week, game_state)


def get_standard_tasks(week, game_state=None):
    """Tasks for Quick Start and Lifetime scenarios"""
    
    tasks = {
        2: [  # Week 2
            {
                "id": "week2_first_visit",
                "type": "sales",
                "title": "👋 Pierwsza wizyta z jakością",
                "description": "Wykonaj wizytę u klienta z oceną min. 3⭐",
                "assigned_by": "Manager",
                "priority": "HIGH",
                "requirements": {
                    "type": "visit_quality",
                    "min_quality": 3,
                    "count": 1
                },
                "reward": {
                    "xp": 100,
                    "unlock_tokens": 2,
                    "client_reputation": 5,
                    "company_reputation": 3,
                    "training_credits": 0
                },
                "story": {
                    "intro": "📞 Manager: 'Onboarding zakończony! Czas na pierwszą prawdziwą wizytę. Postaraj się o min. 3 gwiazdki - to otworzy ci kolejne zadania.'",
                    "completion": "🎉 Pierwsza wizyta zaliczona! Manager jest pod wrażeniem twojego podejścia.",
                    "failure": "Spróbuj ponownie w następnym tygodniu. Jakość wizyt to podstawa!"
                }
            },
            {
                "id": "week2_prospect_outreach",
                "type": "relationship",
                "title": "📞 Odwiedź 5 prospectów",
                "description": "Wykonaj wizyty u 5 nowych klientów (status PROSPECT)",
                "assigned_by": "Manager",
                "priority": "MEDIUM",
                "requirements": {
                    "type": "prospect_visits",
                    "count": 5
                },
                "reward": {
                    "xp": 50,
                    "unlock_tokens": 1,
                    "client_reputation": 3,
                    "company_reputation": 0,
                    "training_credits": 0
                },
                "story": {
                    "intro": "Manager: 'Poznaj teren - odwiedź 5 prospectów. Nie musisz sprzedawać, po prostu przedstaw się i zbadaj potrzeby.'",
                    "completion": "Dobra robota! Poznałeś teren i potencjalnych klientów.",
                    "failure": "Teren pozostaje nieznany. Następnym razem więcej wizyt!"
                }
            }
        ],
        
        3: [  # Week 3
            {
                "id": "week3_first_contract",
                "type": "sales",
                "title": "✍️ Podpisz pierwszą umowę",
                "description": "Zmień status klienta z PROSPECT na ACTIVE (pierwsza sprzedaż)",
                "assigned_by": "Regional Manager",
                "priority": "HIGH",
                "requirements": {
                    "type": "client_activation",
                    "count": 1
                },
                "reward": {
                    "xp": 200,
                    "unlock_tokens": 3,
                    "client_reputation": 10,
                    "company_reputation": 5,
                    "training_credits": 0
                },
                "story": {
                    "intro": "📞 Szef regionu: 'Dobra robota z wizytami! Teraz konkret - przynieś mi podpisaną umowę do piątku. Pokażmy headquarters że warto w ciebie inwestować!'",
                    "completion": "🎉 Pierwsza umowa! Szef: 'Świetnie! Teraz czas na skalowanie. Nowe zadania już czekają.'",
                    "failure": "Nie udało się w tym tygodniu. Pamiętaj: wartość dla klienta, słuchanie potrzeb, rozwiązywanie problemów!"
                }
            },
            {
                "id": "week3_portfolio_mix",
                "type": "sales",
                "title": "📦 Sprzedaj 3 różne kategorie",
                "description": "Sprzedaj produkty z minimum 3 różnych kategorii (np. Personal Care, Food, Snacks)",
                "assigned_by": "Product Manager",
                "priority": "MEDIUM",
                "requirements": {
                    "type": "category_diversity",
                    "min_categories": 3
                },
                "reward": {
                    "xp": 100,
                    "unlock_tokens": 2,
                    "client_reputation": 0,
                    "company_reputation": 3,
                    "training_credits": 0
                },
                "story": {
                    "intro": "Product Manager: 'Marketing chce przetestować cross-category selling. Pokaż że nasze portfolio się uzupełnia - 3 różne kategorie do piątku!'",
                    "completion": "Doskonale! Portfolio diversity to klucz do większych zamówień.",
                    "failure": "Spróbuj ponownie - klient kupujący z wielu kategorii to lojalny klient!"
                }
            }
        ],
        
        4: [  # Week 4
            {
                "id": "week4_sales_target",
                "type": "sales",
                "title": "💰 Sprzedaż 5,000 PLN",
                "requirements": {
                    "type": "weekly_sales",
                    "target": 5000
                },
                "reward": {
                    "xp": 200,
                    "unlock_tokens": 3,
                    "client_reputation": 0,
                    "company_reputation": 10,
                    "training_credits": 0
                },
                "story": {
                    "intro": "📞 Szef: 'Headquarters patrzy na liczby. 5k PLN do piątku - pokaż że jesteś warty awansu!'",
                    "completion": "🎉 Cel osiągnięty! Szef zgłasza cię do programu Fast Track.",
                    "failure": "Nie udało się tym razem. Analizuj co poszło nie tak - volume vs margin, frequency, upselling."
                }
            },
            {
                "id": "week4_relationship",
                "type": "relationship",
                "title": "❤️ Reputacja +50 z 3 klientami",
                "description": "Doprowadź 3 aktywnych klientów do reputacji +50 lub wyższej",
                "requirements": {
                    "type": "client_reputation",
                    "threshold": 50,
                    "count": 3
                },
                "reward": {
                    "xp": 150,
                    "unlock_tokens": 2,
                    "client_reputation": 8,
                    "company_reputation": 0,
                    "training_credits": 0
                },
                "story": {150
                },
                "story": {
                    "intro": "CSM: 'Lojalność = powtarzalne zamówienia. Wybierz 3 klientów i zbuduj z nimi relację. Wizyty, telefony, wsparcie - all in!'",
                    "completion": "Świetnie! Lojalni klienci to fundament twojego biznesu.",
                    "failure": "Relacje wymagają czasu i uwagi. Regularność to klucz!"
                }
            }
        ],
        
        5: [  # Week 5
            {
                "id": "week5_active_clients",
                "type": "sales",
                "title": "🏆 Osiągnij 5 aktywnych klientów",
                "description": "Zbuduj portfolio 5 aktywnych klientów (status ACTIVE)",
                "assigned_by": "Territory Manager",
                "priority": "HIGH",
                "requirements": {
                    "type": "active_clients_count",
                    "target": 5
                },
                "reward": {
                    "xp": 250,
                    "unlock_tokens": 3,
                    "client_reputation": 0,
                    "company_reputation": 8,
                    "training_credits": 0
                },
                "story": {
                    "intro": "Territory Manager: 'Czas na solidną bazę. 5 aktywnych klientów to minimum dla stabilnego terenu.'",
                    "completion": "Baza zbudowana! Territory Manager: 'Teraz czas na jakość obsługi.'",
                    "failure": "Kontynuuj budowanie portfolio. Każdy klient to inwestycja w przyszłość!"
                }
            }
        ],
        
        6: [  # Week 6
            {
                "id": "week6_sales_growth",
                "type": "sales",
                "title": "📈 Sprzedaż 8,000 PLN",
                "description": "Zwiększ tygodniową sprzedaż do 8,000 PLN",
                "assigned_by": "Regional Manager",
                "priority": "HIGH",
                "requirements": {
                    "type": "weekly_sales",
                    "target": 8000
                },
                "reward": {
                    "xp": 250,
                    "unlock_tokens": 3,
                    "client_reputation": 0,
                    "company_reputation": 10,
                    "training_credits": 0
                },
                "story": {
                    "intro": "📞 Szef: 'Czas na wzrost! 8k PLN tym razem. Pokaż że umiesz skalować!'",
                    "completion": "🎉 Wzrost osiągnięty! Szef: 'Widzę progres. Tak trzymaj!'",
                    "failure": "Przeanalizuj: więcej klientów? Większe zamówienia? Upselling?"
                }
            }
        ]
    }
    
    return tasks.get(week, [])


def get_heinz_tasks(week, game_state=None):
    """Tasks specific to Heinz Food Service scenario"""
    
    tasks = {
        2: [  # Week 2
            {
                "id": "heinz_week2_first_visit",
                "type": "sales",
                "title": "👋 Pierwsza wizyta Food Service",
                "description": "Wykonaj wizytę u klienta Food Service z oceną min. 3⭐",
                "assigned_by": "Commercial Director (Paweł)",
                "priority": "HIGH",
                "requirements": {
                    "type": "visit_quality",
                    "min_quality": 3,
                    "count": 1
                },
                "reward": {
                    "xp": 100,
                    "unlock_tokens": 2,
                    "client_reputation": 5,
                    "company_reputation": 3,
                    "training_credits": 0
                },
                "story": {
                    "intro": "📞 Paweł (Commercial Director): 'Trial zakończony! Czas na prawdziwe Food Service. Odwiedź klienta - burger joint, pizzeria, cokolwiek. Pokaż kim jesteś!'",
                    "completion": "🎉 Świetny start! Paweł: 'Widzę potencjał. Kolejne zadania już czekają.'",
                    "failure": "Następnym razem lepiej. Food Service to wymagający kanał!"
                }
            },
            {
                "id": "heinz_week2_kotlin_intel",
                "type": "competitive",
                "title": "🔍 Zbadaj konkurencję (Kotlin)",
                "description": "Odwiedź 3 klientów używających Kotlin i zrób notatki o ich potrzebach",
                "assigned_by": "Commercial Director (Paweł)",
                "priority": "HIGH",
                "requirements": {
                    "type": "competitor_intel",
                    "competitor": "kotlin",
                    "visits": 3,
                    "notes_required": True
                },
                "reward": {
                    "xp": 150,
                    "unlock_tokens": 2,
                    "client_reputation": 0,
                    "company_reputation": 5,
                    "training_credits": 0
                },
                "story": {
                    "intro": "📞 Paweł: 'Headquarters chce wiedzieć dlaczego Kotlin jest silny w Dzięgielowie. Odwiedź 3 sklepy z Kotlin, zrób notatki: dlaczego wybrali Kotlin? Jakie pain points? Potrzebuję tego na czwartek (meeting z HQ)!'",
                    "completion": "Doskonały intel! Paweł: 'To jest wartościowe. HQ daje zielone światło na Kotlin Crush Campaign.'",
                    "failure": "Brak danych to brak strategii. Spróbuj ponownie!"
                }
            }
        ],
        
        3: [  # Week 3
            {
                "id": "heinz_week3_first_contract",
                "type": "sales",
                "title": "✍️ Pierwsza umowa (Heinz lub Pudliszki)",
                "description": "Podpisz pierwszą umowę - może być Heinz Premium lub Pudliszki Value",
                "assigned_by": "Commercial Director (Paweł)",
                "priority": "CRITICAL",
                "requirements": {
                    "type": "client_activation",
                    "count": 1
                },
                "reward": {
                    "xp": 250,
                    "unlock_tokens": 3,
                    "client_reputation": 15,
                    "company_reputation": 10,
                    "training_credits": 0
                },
                "story": {
                    "intro": "📞 Paweł: 'Czas na konkret. Pierwsza umowa do piątku - Heinz, Pudliszki, obojętne. Pokaż że umiesz zamykać!'",
                    "completion": "🎉 Pierwsza krew! Paweł: 'Świetnie! Odblokowuję ci POS materials i competitive pricing. Teraz czas na Kotlin Hunt!'",
                    "failure": "Nie poddawaj się. Każde NIE to krok bliżej TAK!"
                }
            },
            {
                "id": "heinz_week3_kotlin_first_win",
                "type": "competitive",
                "title": "🥊 Przejmij pierwszego klienta od Kotlin",
                "description": "Zamień Kotlin na Heinz/Pudliszki w jednym lokalu",
                "assigned_by": "Marketing Director (Anna)",
                "priority": "HIGH",
                "requirements": {
                    "type": "competitor_win",
                    "competitor": "kotlin",
                    "count": 1
                },
                "reward": {
                    "xp": 300,
                    "unlock_tokens": 5,
                    "client_reputation": 10,
                    "company_reputation": 8,
                    "training_credits": 0
                },
                "story": {
                    "intro": "📧 Anna (Marketing): 'Twój intel był świetny. HQ uruchamia Kotlin Crush Campaign. Pierwsze zadanie: przejmij 1 klienta. Easy targets: Kebab Express (delivery problems), Pizza House (quality issues).'",
                    "completion": "🎉 Pierwszy Kotlin down! Anna: 'Excellent! Campaign oficjalnie rusza. Bonus: access do conversion bundle pricing.'",
                    "failure": "Kotlin jest tough. Użyj FOZ technique, pokaż cost per portion!"
                }
            }
        ],
        
        4: [  # Week 4
            {
                "id": "heinz_week4_distribution",
                "type": "sales",
                "title": "🎯 Dystrybucja: 8 punktów",
                "description": "Osiągnij 8 aktywnych punktów sprzedaży (32% z 25 dostępnych)",
                "assigned_by": "Commercial Director (Paweł)",
                "priority": "HIGH",
                "requirements": {
                    "type": "active_clients_count",
                    "target": 8
                },
                "reward": {
                    "xp": 300,
                    "unlock_tokens": 3,
                    "client_reputation": 0,
                    "company_reputation": 10,
                    "training_credits": 0
                },
                "story": {
                    "intro": "📞 Paweł: 'Distribution is king! 8 punktów do piątku. Mix segmentów: burgery, kebaby, pizzerie. Show me coverage!'",
                    "completion": "Solidna dystrybucja! Paweł: 'Widzę że rozumiesz Food Service. Next level!'",
                    "failure": "Distribution wymaga czasu. Każdy segment to inna strategia!"
                }
            },
            {
                "id": "heinz_week4_kotlin_campaign",
                "type": "competitive",
                "title": "🥊 Kotlin Campaign: 3 przejęcia",
                "description": "Przejmij 3 z 8 klientów Kotlin (milestone: 50%)",
                "assigned_by": "Marketing Director (Anna)",
                "priority": "HIGH",
                "requirements": {
                    "type": "competitor_win",
                    "competitor": "kotlin",
                    "count": 3
                },
                "reward": {
                    "xp": 500,
                    "unlock_tokens": 5,
                    "client_reputation": 15,
                    "company_reputation": 15,
                    "training_credits": 1
                },
                "story": {
                    "intro": "📧 Anna: 'Campaign nabiera tempa. 3 przejęcia do piątku = 50% celu. Masz wszystkie narzędzia: competitive pricing, conversion bundle, POS materials. Go!'",
                    "completion": "🎉 Połowa drogi! Anna: 'HQ jest impressed. Bonus approved. Zostało 3 do 6/8 challenge!'",
                    "failure": "Kotlin fight is tough. Regroup, analyze, attack again!"
                }
            }
        ],
        
        5: [  # Week 5
            {
                "id": "heinz_week5_sales_target",
                "type": "sales",
                "title": "💰 Sprzedaż 10,000 PLN",
                "description": "Osiągnij tygodniową sprzedaż 10k PLN (Heinz + Pudliszki)",
                "assigned_by": "Commercial Director (Paweł)",
                "priority": "HIGH",
                "requirements": {
                    "type": "weekly_sales",
                    "target": 10000
                },
                "reward": {
                    "xp": 350,
                    "unlock_tokens": 4,
                    "client_reputation": 0,
                    "company_reputation": 12,
                    "training_credits": 0
                },
                "story": {
                    "intro": "📞 Paweł: 'Numbers time! 10k PLN tym razem. Mix Heinz premium + Pudliszki volume. Show me you can sell!'",
                    "completion": "🎉 10k milestone! Paweł: 'Świetna sprzedaż. Headquarters noticed!'",
                    "failure": "Analyze mix: premium vs value, volume vs margin. Next week better!"
                }
            }
        ],
        
        6: [  # Week 6
            {
                "id": "heinz_week6_kotlin_final",
                "type": "competitive",
                "title": "🏆 Kotlin Final Push: 6/8",
                "description": "Finalizuj Kotlin Challenge - przejmij 6 z 8 klientów",
                "assigned_by": "CEO & Marketing Director",
                "priority": "CRITICAL",
                "requirements": {
                    "type": "competitor_win",
                    "competitor": "kotlin",
                    "count": 6
                },
                "reward": {
                    "xp": 1000,
                    "unlock_tokens": 10,
                    "client_reputation": 20,
                    "company_reputation": 20,
                    "training_credits": 2
                },
                "story": {
                    "intro": "📞 Paweł + CEO na linii: 'Final week Kotlin Campaign. 6/8 = 10k bonus + Kotlin Slayer achievement. Excellence (8/8) = 15k. HQ obserwuje. Powodzenia!'",
                    "completion": "🎉🏆 KOTLIN CRUSHED! CEO: 'Exceptional work! Top 1% salespeople. Promotion pending. Welcome to elite!'",
                    "failure": "Good effort! Kotlin dominacja złamana, nawet jeśli nie 6/8. Respect!"
                }
            }
        ]
    }
    
    return tasks.get(week, [])


def create_task_from_template(template, assigned_date):
    """
    Create a task instance from template with dates.
    
    Args:
        template: Task dictionary from get_weekly_tasks()
        assigned_date: Date when task was assigned (datetime)
    
    Returns:
        Complete task object ready for session_state
    """
    
    # Calculate deadline (Friday same week)
    days_until_friday = (4 - assigned_date.weekday()) % 7
    if days_until_friday == 0:
        days_until_friday = 7  # If today is Friday, deadline next Friday
    deadline = assigned_date + timedelta(days=days_until_friday)
    
    task = {
        **template,
        "assigned_date": assigned_date.strftime("%Y-%m-%d"),
        "deadline": deadline.strftime("%Y-%m-%d"),
        "progress": {
            "current": 0,
            "target": template["requirements"].get("count") or template["requirements"].get("target", 1),
            "percentage": 0
        },
        "status": "active",  # active, completed, failed, locked
        "completed_date": None,
        "completion_method": "auto"  # auto or manual
    }
    
    return task


def check_task_completion(task, game_state, clients):
    """
    Auto-check if task requirements are met.
    Updates task progress and status.
    
    Args:
        task: Task object
        game_state: Current game state
        clients: Clients dictionary
    
    Returns:
        bool: True if task was just completed this check
    """
    
    if task["status"] != "active":
        return False
    
    req_type = task["requirements"]["type"]
    just_completed = False
    
    # Different check logic based on requirement type
    if req_type == "visit_quality":
        # Check recent visits with min quality
        recent_visits = game_state.get("visits_this_week", [])
        quality_visits = [v for v in recent_visits if v.get("quality", 0) >= task["requirements"]["min_quality"]]
        task["progress"]["current"] = len(quality_visits)
        
    elif req_type == "prospect_visits":
        # Count visits to PROSPECT clients
        prospect_visits = game_state.get("prospect_visits_this_week", 0)
        task["progress"]["current"] = prospect_visits
        
    elif req_type == "client_activation":
        # Count new ACTIVE clients this week
        activations = game_state.get("activations_this_week", 0)
        task["progress"]["current"] = activations
        
    elif req_type == "category_diversity":
        # Count unique categories sold this week
        categories_sold = set(game_state.get("categories_sold_this_week", []))
        task["progress"]["current"] = len(categories_sold)
        
    elif req_type == "weekly_sales":
        # Check weekly revenue
        weekly_sales = game_state.get("weekly_sales", 0)
        task["progress"]["current"] = weekly_sales
        
    elif req_type == "client_reputation":
        # Count clients with reputation >= threshold
        high_rep_clients = sum(
            1 for c in clients.values()
            if c.get("status") == "ACTIVE" and c.get("reputation", 0) >= task["requirements"]["threshold"]
        )
        task["progress"]["current"] = high_rep_clients
        
    elif req_type == "active_clients_count":
        # Count ACTIVE clients
        active_count = sum(1 for c in clients.values() if c.get("status") == "ACTIVE")
        task["progress"]["current"] = active_count
        
    elif req_type == "competitor_intel":
        # Check notes on competitor clients
        competitor = task["requirements"]["competitor"]
        intel_visits = game_state.get(f"intel_visits_{competitor}", 0)
        task["progress"]["current"] = intel_visits
        
    elif req_type == "competitor_win":
        # Count clients won from competitor
        competitor = task["requirements"]["competitor"]
        wins = game_state.get(f"wins_from_{competitor}", 0)
        task["progress"]["current"] = wins
    
    # Update progress percentage
    if task["progress"]["target"] > 0:
        task["progress"]["percentage"] = min(100, int(task["progress"]["current"] / task["progress"]["target"] * 100))
    
    # Check if completed
    if task["progress"]["current"] >= task["progress"]["target"]:
        if task["status"] == "active":  # Just completed
            task["status"] = "completed"
            task["completed_date"] = datetime.now().strftime("%Y-%m-%d")
            just_completed = True
    
    return just_completed


def payout_task_reward(task, game_state, clients):
    """
    Give rewards to player for completing task.
    Modifies game_state in place.
    
    Args:
        task: Completed task object
        game_state: Game state to modify
        clients: Clients dict (for reputation boost)
    
    Returns:
        dict: Summary of rewards given
    """
    from utils.reputation_system import (
        calculate_overall_rating,
        get_tier,
        update_company_reputation_component
    )
    
    reward = task["reward"]
    summary = {}
    
    # XP
    if reward.get("xp"):
        game_state["xp"] = game_state.get("xp", 0) + reward["xp"]
        summary["xp"] = reward["xp"]
        
        # Check level up
        current_level = game_state.get("level", 1)
        xp_for_next = current_level * 1000  # 1000 XP per level
        if game_state["xp"] >= xp_for_next:
            game_state["level"] = current_level + 1
            summary["level_up"] = True
    
    # Unlock Tokens
    if reward.get("unlock_tokens"):
        if "reputation" not in game_state:
            game_state["reputation"] = {}
        game_state["reputation"]["unlock_tokens"] = (
            game_state["reputation"].get("unlock_tokens", 0) + reward["unlock_tokens"]
        )
        summary["unlock_tokens"] = reward["unlock_tokens"]
    
    # Client Reputation boost (dla wszystkich aktywnych klientów)
    if reward.get("client_reputation"):
        boost = reward["client_reputation"]
        count = 0
        for client in clients.values():
            if client.get("status") == "ACTIVE":
                client["reputation"] = client.get("reputation", 50) + boost
                count += 1
        summary["client_reputation_boost"] = boost
        summary["clients_affected"] = count
    
    # Company Reputation boost (Task Performance)
    if reward.get("company_reputation"):
        boost = reward["company_reputation"]
        update_company_reputation_component(
            game_state, 
            "task_performance", 
            boost
        )
        summary["company_reputation_boost"] = boost
    
    # Training Credits
    if reward.get("training_credits") and reward["training_credits"] > 0:
        if "reputation" not in game_state:
            game_state["reputation"] = {}
        game_state["reputation"]["training_credits"] = (
            game_state["reputation"].get("training_credits", 0) + reward["training_credits"]
        )
        summary["training_credits"] = reward["training_credits"]
    
    # Recalculate overall rating and tier
    old_rating = game_state.get("reputation", {}).get("overall_rating", 0)
    old_tier = game_state.get("reputation", {}).get("tier", "Trainee")
    
    new_rating = calculate_overall_rating(game_state, clients)
    new_tier = get_tier(new_rating)
    
    if "reputation" not in game_state:
        game_state["reputation"] = {}
    
    game_state["reputation"]["overall_rating"] = new_rating
    game_state["reputation"]["tier"] = new_tier
    
    summary["rating_change"] = new_rating - old_rating
    if new_tier != old_tier:
        summary["tier_up"] = new_tier
    
    return summary

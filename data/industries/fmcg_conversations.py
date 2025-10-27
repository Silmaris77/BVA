"""
System rozmów AI z klientami FMCG
Wzorowany na Consulting Conversations, ale z pamięcią historii współpracy
"""

def build_conversation_prompt(customer, conversation_history, player_message, context, current_messages=None):
    """
    Buduje prompt dla AI do rozmowy z klientem
    
    Args:
        customer: dict - dane klienta z fmcg_customers.py
        conversation_history: list - lista poprzednich rozmów (spotkań)
        player_message: str - aktualna wiadomość gracza
        context: dict - kontekst (produkty FreshLife, aktualny status współpracy, etc.)
        current_messages: list - historia wiadomości z BIEŻĄCEJ rozmowy
    
    Returns:
        str - prompt dla AI
    """
    
    # Podstawowe info o kliencie
    customer_context = f"""
KLIENT: {customer['name']}
Właściciel: {customer['owner']}
Typ: {customer['type']}
Lokalizacja: {customer['location']}
    
CHARAKTERYSTYKA KLIENTA:
{customer['description']}

Miesięczny obrót: {customer['characteristics']['monthly_revenue']}
Klienci dziennie: {customer['characteristics']['customers_per_day']}
Konkurencja: {customer['characteristics']['competition']}

OSOBOWOŚĆ właściciela:
Styl: {customer['personality']['style']}
Priorytety: {', '.join(customer['personality']['priorities'])}
Obawy: {', '.join(customer['personality']['concerns'])}
Styl negocjacji: {customer['personality']['negotiation_style']}
"""
    
    # Historia współpracy (jeśli istnieje)
    history_context = ""
    if conversation_history:
        history_context = "\n\nHISTORIA WSPÓŁPRACY:\n"
        for idx, conv in enumerate(conversation_history[-3:], 1):  # Ostatnie 3 rozmowy
            history_context += f"""
Spotkanie #{idx} ({conv.get('date', 'brak daty')}):
Temat: {conv.get('topic', 'brak tematu')}
Ustalenia: {conv.get('agreements', 'brak ustaleń')}
Następne kroki: {conv.get('next_steps', 'brak')}
Wrażenie klienta: {conv.get('customer_impression', 'neutralne')}
"""
    
    # Status współpracy
    status = context.get('relationship_status', 'prospect')
    products_sold = context.get('products_sold', [])
    
    status_context = f"""
STATUS WSPÓŁPRACY: {status}
Produkty w sprzedaży: {', '.join(products_sold) if products_sold else 'Brak - pierwsza rozmowa'}
Relationship score: {context.get('relationship_score', 0)}/100
"""
    
    # Bieżąca rozmowa (kontekst dla AI)
    current_conversation_context = ""
    if current_messages and len(current_messages) > 0:
        current_conversation_context = "\n\nBIEŻĄCA ROZMOWA (pamiętaj co już zostało powiedziane):\n"
        # Pokaż wszystkie wiadomości z bieżącej rozmowy OPRÓCZ ostatniej (bo ona jest w "Gracz pisze")
        for msg in current_messages[:-1]:  # Exclude last message (it's the player_message)
            role_label = "Handlowiec" if msg['role'] == 'player' else "Ty"
            current_conversation_context += f"{role_label}: {msg['content']}\n\n"

    # Prompt systemowy
    system_prompt = f"""
Jesteś {customer['owner']}, właścicielem {customer['name']}.

{customer_context}

{status_context}

{history_context}

{current_conversation_context}

TWOJA ROLA:
- Grasz osobę właściciela sklepu w realistyczny sposób
- Pamiętasz poprzednie rozmowy i ustalenia
- PAMIĘTASZ CO POWIEDZIAŁEŚ W BIEŻĄCEJ ROZMOWIE - nie powtarzaj się
- Jeśli już się przywitałeś - NIE witaj się ponownie
- Jeśli gracz obiecał coś wcześniej i nie dotrzymał - przypominasz mu o tym
- Twoje decyzje są spójne z charakterem właściciela i sytuacją sklepu
- Negocjujesz zgodnie ze swoim stylem (twardo/miękko/analitycznie)

ZASADY ROZMOWY:
1. Bądź autentyczny - mów jak prawdziwy właściciel sklepu
2. Reaguj na to co gracz mówi - nie mów ogólników
3. Jeśli już się przywitaliście na początku tej rozmowy - NIE powtarzaj powitania
4. Jeśli gracz oferuje produkty - pytaj o szczegóły (marża, MOQ, wsparcie)
5. Jeśli gracz próbuje Cię manipulować - dostrzegaj to
6. Pamiętaj poprzednie ustalenia i przypominaj o nich
7. Twoje decyzje muszą mieć sens biznesowy dla Twojego sklepu

TWOJA WYPOWIEDŹ:
- Odpowiadaj jak prawdziwy człowiek (krótko lub długo, zależnie od sytuacji)
- Używaj języka potocznego, naturalnego
- Nie używaj bullet points - mów normalnie
- Możesz wyrażać emocje (zadowolenie, frustrację, podekscytowanie)

Gracz pisze:
"{player_message}"

Odpowiedz jako {customer['owner']} (kontynuuj rozmowę, NIE zaczynaj od nowa):
"""
    
    return system_prompt


def evaluate_conversation_outcome(conversation_text, customer, context):
    """
    Ocenia rezultat rozmowy (czy gracz osiągnął cel, jak zareagował klient)
    
    Returns:
        dict - wynik rozmowy
    """
    # To będzie używane do oceny czy gracz:
    # - Zdobył zamówienie
    # - Poprawił relację
    # - Pogorszył relację
    # - Ustalił konkretne next steps
    
    # Na razie placeholder - później dodamy AI evaluation
    return {
        "relationship_change": 0,  # -20 do +20
        "deal_closed": False,
        "agreements": [],
        "next_steps": [],
        "customer_impression": "neutral"  # positive, neutral, negative
    }

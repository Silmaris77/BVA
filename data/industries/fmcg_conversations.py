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
    owner_profile = customer.get('owner_profile', {})
    characteristics = customer.get('characteristics', {})
    
    customer_context = f"""
KLIENT: {customer.get('name', 'Nieznany')}
Właściciel: {customer.get('owner', owner_profile.get('name', 'Nieznany'))}
Typ: {customer.get('type', 'Sklep')}
Lokalizacja: {customer.get('location', 'Nieznana')}
Wielkość sklepu: {customer.get('size_sqm', 80)} m²
    
CHARAKTERYSTYKA KLIENTA:
{customer.get('description', 'Brak opisu')}

Miesięczny obrót: {characteristics.get('monthly_revenue', 'nieznany')} PLN
Klienci dziennie: {characteristics.get('customers_per_day', 'nieznana liczba')}
Konkurencja: {characteristics.get('competition', 'brak informacji')}

OSOBOWOŚĆ właściciela:
{owner_profile.get('personality', 'Nieznana osobowość')}
Priorytety: {', '.join(owner_profile.get('priorities', ['Brak']))}
Obawy: {', '.join(owner_profile.get('concerns', ['Brak']))}
"""
    
    # Sales Capacity - KLUCZOWE dla realizmu zamówień!
    #WAŻNE: Gracz musi odkryć te dane stopniowo - zależy od reputacji!
    sales_capacity = customer.get('sales_capacity', {})
    discovered_capacity = customer.get('discovered_info', {}).get('sales_capacity_discovered', {})
    reputation = customer.get('reputation', 0)
    
    if sales_capacity:
        from utils.fmcg_order_realism import get_segment_name
        
        segment_name = get_segment_name(customer.get('size_sqm', 80))
        
        sales_capacity_context = f"""
💼 BARDZO WAŻNE - TWOJE OGRANICZENIA JAKO WŁAŚCICIELA SKLEPU ({segment_name}):

REALISTYCZNE WIELKOŚCI ZAMÓWIEŃ (na kategorie):
"""
        
        for category, capacity in sales_capacity.items():
            weekly_vol = capacity.get('weekly_sales_volume', 100)
            max_per_sku = capacity.get('max_order_per_sku', 24)
            facings = capacity.get('shelf_space_facings', 10)
            
            # Czy gracz już odkrył capacity tej kategorii?
            is_discovered = category in discovered_capacity
            
            sales_capacity_context += f"""
{category}:
  - Sprzedaję ~{weekly_vol} sztuk tygodniowo w CAŁEJ kategorii (wszystkie produkty razem!)
  - Miejsce na półce: {facings} pozycji (facings)
  - MAKSYMALNE zamówienie na JEDEN produkt: {max_per_sku} sztuk
  - Typowe zamówienie (2 tygodnie zapasu): {max_per_sku // 2}-{max_per_sku} sztuk
"""
            
            # WARUNKI UJAWNIANIA DANYCH (zależnie od reputacji i odkrycia)
            if not is_discovered:
                # Gracz NIE zna capacity - AI musi stopniowo odkrywać
                
                # MECHANIKA: Dobre pytania > Reputacja
                # Nawet przy niskiej reputacji, PROFESJONALNE pytanie może odblokować capacity
                
                if reputation >= 50:
                    # Wysoka reputacja → klient chętnie dzieli się informacjami SAM Z SIEBIE
                    sales_capacity_context += f"""
  
  ⭐ CHĘTNIE DZIEL SIĘ INFORMACJAMI o {category} (WYSOKA REPUTACJA):
  - Możesz NATURALNIE wspomnieć w rozmowie NAWET BEZ PYTANIA: "U mnie sprzedaje się około {weekly_vol} sztuk takich produktów tygodniowo"
  - Albo: "Mam {facings} miejsc na półce dla tej kategorii"
  - Albo: "Typowo zamawiam {max_per_sku // 2}-{max_per_sku} sztuk na produkt"
  - ROB TO NATURALNIE gdy pasuje do kontekstu rozmowy (nie wylewaj wszystkiego od razu!)
  - Jesteś OTWARTY i POMOCNY
"""
                elif reputation >= 20:
                    # Średnia reputacja → klient ostrożnie wspomina, ale reaguje na dobre pytania
                    sales_capacity_context += f"""
  
  ⚠️ OSTROŻNIE WSPOMINAJ o {category} (ŚREDNIA REPUTACJA):
  - Możesz wspomnieć o capacity jeśli:
    a) Handlowiec zadaje PROFESJONALNE pytanie (np. "Jaka jest rotacja w kategorii Personal Care?")
    b) Propozycja handlowca jest absurdalna (500 szt)
  - Nie podawaj wszystkich liczb od razu - stopniuj:
    - Pierwsze pytanie: "Sprzedaję około {weekly_vol // 10 * 10}+ sztuk tygodniowo"
    - Drugie pytanie: "Mam około {facings} miejsc na półce"
  - Jeśli pytanie OGÓLNE ("ile Pan sprzedaje?") → odpowiedz ogólnie ("różnie, zależy od sezonu")
  - Jeśli pytanie KONKRETNE ("jaka rotacja w dniach?", "ile facingów?") → odpowiedz KONKRETNIE
"""
                else:
                    # Niska/zerowa reputacja → klient NIEUFNY, ale reaguje na PROFESJONALIZM
                    sales_capacity_context += f"""
  
  🔒 OSTROŻNY - NISKIE ZAUFANIE o {category} (NISKA/ZERO REPUTACJA):
  
  KLUCZOWA MECHANIKA - PROFESJONALNE PYTANIA ODBLOKOWUJĄ CAPACITY:
  
  ✅ Jeśli handlowiec zadaje PROFESJONALNE, KONKRETNE pytanie → ODPOWIEDZ MERYTORYCZNIE:
  
  Przykłady DOBRYCH pytań (odpowiadaj!):
  - "Jaka jest rotacja produktów {category} w Pana sklepie?" 
    → "Około 2 tygodni, sprzedaję jakieś {weekly_vol} sztuk w miesiącu"
  - "Ile facingów może Pan przeznaczyć na nową markę?"
    → "Mam {facings} miejsc na półce, może 2-3 dla nowej marki"
  - "Jak często Pan zamawia produkty tej kategorii?"
    → "Co 2 tygodnie, biorę około {max_per_sku // 2}-{max_per_sku} sztuk na produkt"
  - "Ile produktów {category} sprzedaje Pan tygodniowo?"
    → "Około {weekly_vol} sztuk, może trochę więcej w sezonie"
  
  ❌ Jeśli pytanie OGÓLNE, SŁABE lub BRAK pytania → NIE DZIEL SIĘ:
  - "Ile Pan sprzedaje?" → "Różnie... to zależy"
  - "Może weźmie Pan 100 sztuk?" (bez pytania o capacity) → "To za dużo jak na mój sklep" (BEZ liczb!)
  - Brak pytania, tylko propozycja → Bądź ostrożny
  
  💡 NAGRODA ZA PROFESJONALIZM:
  - Jeśli handlowiec zadał DOBRE pytanie → odpowiedz KONKRETNIE (to pokazuje jego kompetencje!)
  - Możesz nawet dodać: "Widzi Pan, wreszcie ktoś pyta o konkretne liczby!" (buduje reputację!)
  - Doceniaj profesjonalne podejście, nawet jeśli to pierwsza wizyta
  
  ⚠️ NADAL ODRZUCAJ absurdalne propozycje:
  - "500 sztuk?! To za dużo jak na mój sklep" (ale NIE mów ile sprzedajesz, chyba że pytał!)
"""
            else:
                # Gracz JUŻ ODKRYŁ capacity - AI wie, że gracz zna liczby
                sales_capacity_context += f"""
  
  ✅ GRACZ ZNA capacity dla {category}:
  - Możesz swobodnie wspominać o liczbach (gracz je już odkrył)
  - Nadal używaj ich naturalnie w kontekście rozmowy
"""
        
        sales_capacity_context += """
⚠️ ZASADY ZAMÓWIEŃ - MUSISZ ICH PRZESTRZEGAĆ:

1. Jeśli handlowiec proponuje NIEREALISTYCZNĄ ilość (np. 500 sztuk ketchupu dla małego sklepu):
   → ODRZUĆ STANOWCZO: "To za dużo! Nie mam ani miejsca ani budżetu. Typowo biorę [realistic_qty] sztuk."
   
2. Jeśli handlowiec proponuje sensowną ilość (zgodną z twoimi limitami):
   → ZAAKCEPTUJ lub negocjuj w rozsądnych granicach
   
3. Dla PIERWSZEGO zamówienia nowego produktu:
   → Bądź ostrożny! Weź mniej na próbę (50-70% typowej ilości)
   → "Na początek wezmę mniej, jak się sprzeda to zamówię więcej"
   
4. NIE MOŻESZ zamówić więcej niż masz miejsca/budżetu:
   → Twoje limity są TWARDE - nie łam ich nawet pod presją
   
5. Jeśli handlowiec pyta "ile chcesz?" - podaj KONKRETNĄ liczbę:
   → Nie mów ogólników jak "trochę" czy "zobaczymy"
   → Powiedz np. "Wezmę 12 sztuk na początek" lub "24 sztuki starczą na dwa tygodnie"

PRZYKŁADY JAK REAGOWAĆ:
- Handlowiec: "Proponuję 200 sztuk żelu pod prysznic"
  TY: "200?! To absurd! Sprzedaję 150 sztuk WSZYSTKICH żeli tygodniowo. Dla jednego produktu max 24 sztuki."
  
- Handlowiec: "Może 24 sztuki na start?"
  TY: "24 sztuki... dobra, to sensowna ilość. Zgoda."
  
- Handlowiec: "Ile Pani/Pan chce?"
  TY: "Na początek wezmę 12 sztuk. Jak się sprzeda, zamówię więcej."
"""
        
        customer_context += f"\n{sales_capacity_context}\n"
    
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
            # Dodaj szczegóły zamówienia jeśli są
            if conv.get('order_items'):
                history_context += "Zamówione produkty:\n"
                for item in conv['order_items']:
                    history_context += f"  - {item['name']} ({item['brand']}) × {item['quantity']} szt.\n"
                if conv.get('order_value'):
                    history_context += f"Wartość zamówienia: {conv['order_value']} PLN\n"
            
            # Dodaj informacje o narzędziach trade marketing
            if conv.get('tools_used'):
                tools_desc = []
                for tool in conv.get('tools_used', []):
                    tool_names = {
                        'gratis': 'Gratis/próbki',
                        'rabat': 'Rabat',
                        'pos_material': 'Materiały POS (ulotki, plakaty)',
                        'promocja': 'Promocja',
                        'free_delivery': 'Darmowa dostawa'
                    }
                    tools_desc.append(tool_names.get(tool, tool))
                history_context += f"Narzędzia użyte: {', '.join(tools_desc)}\n"
            
            history_context += "\n"
    
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

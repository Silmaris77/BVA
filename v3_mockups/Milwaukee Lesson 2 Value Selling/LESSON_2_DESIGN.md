# Milwaukee Lesson 2: Value Selling - ROI & TCO

## 🎯 Cel Lekcji
Nauczyć KAM jak **kwantyfikować wartość** rozwiązań Milwaukee i **sprzedawać ROI** zamiast ceny. Przekształcać rozmowy o "narzędziu za 2000 PLN" w dyskusje o "oszczędności 50 000 PLN rocznie".

## 📊 Metadane
- **Czas**: ~70 min
- **XP Total**: 95 XP
- **Prerequisite**: Lesson 1 (Discovery) ukończona
- **Badge**: 💰 Value Architect
- **Target**: KAM sprzedający do przemysłu (po ukończeniu Discovery)

---

## 📋 Struktura 10 Kart

### **KARTA 1: Video - Value vs. Price** (5 XP)
**Typ**: Video + Reflection

**Treść**:
- Video (8 min): "Dlaczego przemysł NIE kupuje najtaniej?"
  - Case: Zakład VW Poznań - wybrali Milwaukee mimo 40% wyższej ceny
  - TCO breakdown: narzędzie 2000 PLN, oszczędności 50 000 PLN/rok
  - Psychologia decyzji: CFO patrzy na 3-letni TCO, nie cenę katalogową
  
**Interakcja**:
- Checkbox: "Obejrzałem całe video" (+5 XP)
- Reflection textarea: "Dlaczego Twój klient miałby zapłacić więcej za Milwaukee?"
- Auto-save

**Insight Box**:
"W przemyśle decyzje są podejmowane na podstawie **Total Cost of Ownership**, nie ceny zakupu. Twoja rola: pomóc CFO policzyć ROI."

---

### **KARTA 2: TCO Framework - Koszt ukryty** (0 XP - prezentacja)
**Typ**: Infografika + Tabela

**Treść**:
**3 kolumny**:
| Kategoria | Bosch (tani) | Milwaukee (wartość) |
|-----------|--------------|---------------------|
| **Cena zakupu** | 1200 PLN | 2000 PLN (+67%) |
| **Żywotność** | 2 lata | 5 lat |
| **Downtime** | 8h/rok | 2h/rok |
| **Koszt downtime** | 8h × 500 PLN/h = 4000 PLN/rok | 2h × 500 PLN/h = 1000 PLN/rok |
| **Serwis** | 3× po 300 PLN = 900 PLN/rok | 1× po 200 PLN = 200 PLN/rok |
| **Rotacja operatorów** | 25% (frustracja) | 10% (ergonomia) |
| **Koszt rotacji** | 15% × 60 000 PLN = 9000 PLN/rok | 0% |
| **TCO 3 lata** | **43 100 PLN** | **23 600 PLN** ✅ |
| **Oszczędność** | - | **-45%** (19 500 PLN) |

**Wizualizacja**:
- Iceberg diagram: "Cena zakupu to tylko 5% TCO"
- 95% to: Downtime, Serwis, Szkolenia, Rotacja, Utrata produktywności

**Tooltips**:
- **Downtime**: Czas przestoju linii produkcyjnej (koszt: 500-2000 PLN/h w automotive)
- **Rotacja**: Koszt rekrutacji + szkolenia nowego operatora (50 000-80 000 PLN)
- **TCO**: Total Cost of Ownership (całkowity koszt posiadania przez 3-5 lat)

---

### **KARTA 3: ROI Calculator Interactive** (15 XP)
**Typ**: Kalkulator z formularzem

**Treść**:
Interaktywny kalkulator ROI - user wprowadza dane swojego klienta:

**Input fields** (10 pól):
1. **Liczba narzędzi**: (np. 50 wkrętarek)
2. **Cena konkurencji**: (PLN)
3. **Cena Milwaukee**: (PLN)
4. **Żywotność konkurencji**: (lata)
5. **Żywotność Milwaukee**: (lata)
6. **Downtime konkurencji**: (godzin/rok)
7. **Downtime Milwaukee**: (godzin/rok)
8. **Koszt downtime**: (PLN/h) - tooltip: "Automotive: 500-2000, Mining: 2000-5000, Produkcja: 300-800"
9. **Koszt serwisu konkurencji**: (PLN/rok)
10. **Koszt serwisu Milwaukee**: (PLN/rok)

**Auto-calculation** (live update):
- **Investment difference**: (Milwaukee - konkurencja) × liczba narzędzi
- **Annual savings**: (downtime savings + serwis savings) × liczba narzędzi
- **Payback period**: Investment / Annual savings (w miesiącach)
- **3-year ROI**: ((3 × Annual savings) - Investment) / Investment × 100%
- **5-year NPV**: Net Present Value (z dyskontem 8%)

**Wizualizacja**:
- Bar chart: TCO Year 1, Year 2, Year 3 (konkurencja vs. Milwaukee)
- Line chart: Cumulative savings over time
- Gauge: ROI % (0-500%)

**Validation**:
- Wszystkie 10 pól wypełnione (liczby > 0)
- Milwaukee droższe niż konkurencja (realistyczny scenariusz)

**Output**:
- Podsumowanie: "Inwestycja zwróci się w **X miesięcy**. ROI 3-letni: **Y%**."
- "Zapisz kalkulację" button → +15 XP (pierwszy raz)
- Download PDF mockup (produkcja: prawdziwy PDF)

**Prefilled example** (Mahle case):
- 50 wkrętarek, Bosch 1200 PLN, Milwaukee 2000 PLN
- Payback: 8 miesięcy, ROI 3-letni: 180%

---

### **KARTA 4: Value Proposition Canvas** (10 XP)
**Typ**: Interaktywny canvas (2 kolumny)

**Treść**:
Framework: **Customer Pains → Milwaukee Gains**

**Lewa kolumna**: Bolączki klienta (user wypełnia)
- Textarea 1: **Functional pains** (np. "Wibracje, waga, częste awarie")
- Textarea 2: **Financial pains** (np. "Wysokie koszty serwisu, downtime, rotacja")
- Textarea 3: **Emotional pains** (np. "Frustracja operatorów, presja CFO na koszty")

**Prawa kolumna**: Wartość Milwaukee (user wypełnia)
- Textarea 4: **Pain relievers** (np. "Technologia REDLINK - 0 awarii, ergonomia ONE-KEY")
- Textarea 5: **Gain creators** (np. "Oszczędność 50k/rok, ROI 180%, 5-letnia gwarancja")
- Textarea 6: **Value metrics** (np. "-80% downtime, -60% serwis, +30% produktywność")

**Dropdown examples**:
- Mining (KGHM): Pains = ATEX, odległe kopalnie, brak serwisu → Gains = ATEX certyfikacja, 24/7 support, 5-letnia gwarancja
- Automotive (Mahle): Pains = OEE, rotacja, przestój linii → Gains = ROI 180%, -25% rotacja, track & trace
- Custom: Czyste pola

**Validation**:
- Min 50 znaków w każdym z 6 pól
- Auto-save
- "Zapisz Value Proposition" → +10 XP

**Podpowiedzi**:
- Icon hints obok każdego pola z przykładami
- "Nie sprzedajesz narzędzia, sprzedajesz rozwiązanie konkretnego problemu"

---

### **KARTA 5: Case Study - VW Poznań** (10 XP)
**Typ**: Timeline + Quiz Case

**Treść**:
**Scenariusz**: Ania (KAM Milwaukee) vs. Procurement Manager VW Poznań (Marcin)

**Timeline (6 kroków)**:

**M1: Discovery**
- Ania: Odkrywa pain point - 12h downtime/miesiąc z wkrętarkami pneumatycznymi
- Koszt: 12h × 1500 PLN/h = 18 000 PLN/miesiąc
- Marcin: "Bosch jest 40% tańszy. Dlaczego mam przepłacać?"

**M2: ROI Presentation**
- Ania przygotowuje kalkulator:
  - Inwestycja: +40 000 PLN (Milwaukee droższe)
  - Oszczędność downtime: -144h/rok × 1500 PLN = -216 000 PLN/rok
  - Oszczędność serwisu: -12 000 PLN/rok
  - **Payback: 2.1 miesiąca**
- Marcin: "Nie wierzę w te liczby. Skąd wiesz, że downtime spadnie o 80%?"

**M3: Proof of Concept**
- Ania proponuje 2-tygodniowy pilot na 1 linii (5 wkrętarek)
- Tracking: downtime, produktywność, feedback operatorów
- Koszt pilotu: 0 PLN (Milwaukee pokrywa)

**M4: Pilot Results**
- Downtime: -70% (lepsze niż obietnica!)
- Produktywność: +15% (bonus)
- NPS operatorów: 9/10 ("najlepsze narzędzia ever")
- Marcin: "Impressed. Ale CFO chce 3-letni ROI ≥ 150%."

**M5: CFO Meeting**
- Ania prezentuje 3-letni TCO:
  - Total savings: 684 000 PLN (downtime + serwis + produktywność)
  - Investment: 120 000 PLN
  - **ROI: 470%**
  - NPV: 520 000 PLN (dyskont 8%)
- CFO: "Approved. Ale potrzebuję tracking KPI post-implementacji."

**M6: Deal + Long-term Partnership**
- Kontrakt: 120 000 PLN (60 wkrętarek + akcesoria)
- Ania dostarcza dashboard ONE-KEY: real-time tracking downtime, utilization
- Po 6 miesiącach: downtime -75%, oszczędności 350 000 PLN (on track)
- VW rozszerza kontrakt na 3 inne zakłady → 500 000 PLN deal

**Reflection Questions** (3 pola, min 60 znaków każde):
1. "W którym momencie Ania przekonała Marcina do pilotu?"
2. "Dlaczego CFO wymagał ROI ≥150%? Co to mówi o decision criteria?"
3. "Jak dashboard ONE-KEY pomógł zamknąć deal?"

**Auto-save + validation** → +10 XP

**Key Insight Box**:
"Procurement patrzy na cenę. CFO patrzy na ROI. Twoja strategia: **bypass Procurement, sell to CFO**."

---

### **KARTA 6: Quiz - ROI Scenarios** (15 XP)
**Typ**: Quiz (12 pytań)

**Format**: Scenario-based multiple choice

**Przykładowe pytania**:

**Q1**: Klient mówi: "Bosch jest 30% tańszy. Dlaczego mam przepłacać?"  
Twoja reakcja:
- A) "Milwaukee ma lepszą jakość" (❌ za ogólne)
- B) "Policzmy TCO 3-letni. Bosch może być droższy o 50% w długim terminie" (✅ kwantyfikuj)
- C) "Damy 10% rabat" (❌ walka ceną)
- D) "Wszyscy liderzy rynku wybierają Milwaukee" (❌ argument z autorytetu, nie ROI)

**Q2**: CFO pyta: "Jaki jest payback period?"  
Co odpowiesz:
- A) "Zwykle 12-18 miesięcy" (❌ za ogólne)
- B) "Zależy od utilization" (❌ unikanie odpowiedzi)
- C) "Na podstawie Waszego downtime 12h/miesiąc: **8.5 miesiąca**" (✅ konkretny ROI)
- D) "Nie wiem, to pytanie do finansów" (❌ brak przygotowania)

**Q3**: Procurement Manager mówi: "Potrzebujemy 3 ofert. Konkurencja daje 25% taniej."  
Strategia:
- A) Obniż cenę o 20% żeby wygrać (❌ race to bottom)
- B) "Zaproponujmy pilot 2-tygodniowy - porównajcie downtime" (✅ PoC beats price)
- C) "Nasz produkt jest premium, nie można porównywać" (❌ arogancja)
- D) Wycofaj się z dealu (❌ poddanie się)

**Q4**: Klient: "ROI brzmi super, ale nie mamy budżetu w tym kwartale."  
Co robisz:
- A) Poczekaj do Q2 (❌ stracisz momentum)
- B) Zaproponuj leasing 36-miesięczny z OpEx (✅ finansowanie = enable sale)
- C) Obniż cenę o 30% (❌ marnujesz wartość)
- D) "W takim razie konkurencja wygra" (❌ presja nie działa)

**Q5**: Production Manager jest przekonany, ale CFO blokuje deal.  
Twoja akcja:
- A) Zwiększ presję na Production Managera (❌ internal politics)
- B) Zaproś CFO na prezentację ROI z dashboard (✅ sell to real decision maker)
- C) Obniż cenę o 15% (❌ nie rozwiązuje problemu)
- D) Poczekaj aż CFO zmieni zdanie (❌ pasywność)

**Q6**: Klient pyta: "Ile zaoszczędzimy w ciągu 5 lat?"  
Odpowiedź:
- A) "Około 500k PLN" (❌ za niedokładne, brak credibility)
- B) "Nie mogę obiecać savings" (❌ brak confidence)
- C) "Na podstawie pilotu: **487 000 PLN** (downtime -70%, serwis -60%)" (✅ data-driven)
- D) "To zależy od wielu czynników" (❌ unikanie commitment)

*[...6 więcej pytań o: NPV, dyskontowanie, risk mitigation, competitive positioning, stakeholder buy-in]*

**Scoring**:
- 10-12: "💎 ROI Master - gotowy na każdą obiekcję CFO"
- 7-9: "💰 Solid Value Seller"
- 4-6: "⚠️ Potrzebujesz więcej praktyki z ROI"
- 0-3: "❌ Wróć do materiałów - to podstawy!"

+15 XP przy ukończeniu

---

### **KARTA 7: Objection Handling - 6 klasycznych** (20 XP)
**Typ**: Flashcards z role-play

**Format**: 6 kart (flip cards) z obiekcjami + best practices

**Objection 1: "Za drogo"**
- **Front**: 💸 "Milwaukee jest 40% droższe niż konkurencja"
- **Back**:
  - **Nie mów**: "Jakość kosztuje" / "Damy rabat"
  - **Powiedz**: "Policzmy TCO 3-letni. Ile kosztuje Was 1h downtime? Ile razy w roku narzędzie się psuje? Zmierzmy całkowity koszt posiadania."
  - **Akcja**: Otwórz kalkulator ROI, wypełnij z klientem
  - **Proof**: Case study VW Poznań (-45% TCO mimo +40% ceny)

**Objection 2: "Nie mamy budżetu"**
- **Front**: 💰 "Nie ma budżetu w tym roku"
- **Back**:
  - **Nie mów**: "Poczekam do przyszłego roku"
  - **Powiedz**: "Rozumiem. Ile tracicie miesięcznie przez downtime? (np. 18k PLN) × 12 = **216k PLN/rok straty**. Czy nie lepiej wziąć leasing 1800 PLN/miesiąc i oszczędzić 18k od razu?"
  - **Akcja**: Zaproponuj OpEx leasing (36 miesięcy) zamiast CapEx
  - **Proof**: 70% dealów w automotive to leasing

**Objection 3: "Nie wierzymy w te savings"**
- **Front**: 🤔 "Wasze liczby ROI są zbyt optymistyczne"
- **Back**:
  - **Nie mów**: "Nasze dane są wiarygodne"
  - **Powiedz**: "Zgadzam się - nie wierzcie na słowo. Zróbmy **2-tygodniowy pilot**. Zmierzymy downtime before/after. Jeśli oszczędności będą <50%, wycofam ofertę."
  - **Akcja**: No-risk PoC (0 PLN koszt pilotu)
  - **Proof**: 85% pilotów kończy się dealem (bo dane nie kłamią)

**Objection 4: "Mamy kontrakt z innym dostawcą"**
- **Front**: 🔒 "Jesteśmy związani umową z Bosch przez 2 lata"
- **Back**:
  - **Nie mów**: "W takim razie wrócę za 2 lata"
  - **Powiedz**: "Rozumiem. Ile kosztuje Was **exit clause** w kontrakcie? Porównajmy z oszczędnościami Milwaukee: jeśli oszczędzicie 200k/rok, warto zapłacić 50k penalty i zmienić dostawcę już teraz."
  - **Akcja**: Kalkulacja NPV (switching cost vs. savings)
  - **Proof**: Case study - KGHM przerwał kontrakt mid-term (ROI 300% > penalty cost)

**Objection 5: "CFO nie zgodzi się"**
- **Front**: 👔 "Production Manager chce, ale CFO blokuje"
- **Back**:
  - **Nie mów**: "Przekonajcie CFO"
  - **Powiedz**: "Zaprośmy CFO na **30-minutową prezentację ROI**. Pokażę: payback period, NPV, risk mitigation. Jeśli nie będzie przekonany, odpuszczam."
  - **Akcja**: Direct meeting z CFO (bypass middle managers)
  - **Proof**: 60% dealów wymaga CFO buy-in - nie unikaj, zaproś

**Objection 6: "Competitor ma lepszą ofertę"**
- **Front**: ⚔️ "DeWalt oferuje 20% rabat + darmowe szkolenie"
- **Back**:
  - **Nie mów**: "Damy jeszcze większy rabat"
  - **Powiedz**: "Świetnie! Porównajmy **total package value**: DeWalt 80k PLN + szkolenie (2k) = 82k. Milwaukee 100k + tracking dashboard (10k value) + 5-letnia gwarancja (15k value) + ROI 200k/rok = **-100k investment, +200k savings**. Co wybierzesz?"
  - **Akcja**: Value comparison table (nie price comparison)
  - **Proof**: Mahle wybrał Milwaukee mimo +35% ceny (total value > price)

**Progress tracking**: "Poznane obiekcje: X/6"

**Button po 6/6**: 
- "Znam wszystkie obiekcje" (+20 XP)
- "Przećwicz ponownie"

---

### **KARTA 8: Competitive Positioning Matrix** (10 XP)
**Typ**: Interaktywna tabela porównawcza

**Treść**:
User wypełnia pozycjonowanie Milwaukee vs. 3 konkurentów (Bosch, DeWalt, Hilti)

**12 kryteriów** (kolumny: Milwaukee | Bosch | DeWalt | Hilti):
1. **Cena zakupu** (dropdown: ++/+/=/-)
2. **Żywotność** (dropdown: ++/+/=/-)
3. **Downtime** (dropdown: ++/+/=/-)
4. **Serwis 24/7** (checkbox: TAK/NIE × 4)
5. **Gwarancja** (input: lata)
6. **Track & Trace** (checkbox: TAK/NIE × 4)
7. **ATEX certyfikacja** (checkbox: TAK/NIE × 4)
8. **Ergonomia** (dropdown: ++/+/=/-)
9. **Ecosystem** (ile narzędzi w ofercie)
10. **Szkolenia** (checkbox: TAK/NIE × 4)
11. **ROI documented** (checkbox: TAK/NIE × 4)
12. **Leasing available** (checkbox: TAK/NIE × 4)

**Auto-generate**:
- **Total Score**: Suma punktów (++ = 2, + = 1, = = 0, - = -1)
- **Best for**: Rekomendacja na podstawie profilu (Mining/Automotive/Produkcja)
- **Differentiation Statement**: Auto-generated pitch (np. "Milwaukee wygrywa na żywotności (+50%) i track & trace, ale jest 30% droższy. **Payback: 8 miesięcy** dzięki -70% downtime.")

**Prefilled Example** (Automotive case):
- Milwaukee: Cena -, Żywotność ++, Downtime ++, Track&Trace TAK, Gwarancja 5, ROI documented TAK → Score 9/12
- Bosch: Cena ++, Żywotność +, Downtime +, Track&Trace NIE, Gwarancja 2, ROI documented NIE → Score 5/12

**Validation**:
- Wszystkie 12 kryteriów wypełnione dla Milwaukee + min 2 konkurentów
- "Zapisz positioning" → +10 XP

**Output**:
- PDF Export mockup: "Competitive Matrix - Milwaukee vs. Market"

---

### **KARTA 9: Elevator Pitch Builder** (15 XP)
**Typ**: Mad Libs style sentence builder

**Treść**:
User buduje **30-sekundowy value pitch** wypełniając luki:

**Template**:
"Widzę, że [PAIN POINT] kosztuje Was [KWOTA] rocznie przez [ROOT CAUSE].

Milwaukee rozwiązuje to przez [SOLUTION FEATURE], co daje [MEASURABLE OUTCOME].

Na podstawie podobnego klienta [CASE STUDY REFERENCE], zaoszczędziliście [ROI NUMBER] w ciągu [TIMEFRAME].

Czy moglibyśmy zmierzyć Wasze savings przez [PROPOSED ACTION]?"

**Input fields** (8 pól):
1. **Pain Point** (dropdown: Downtime / Rotacja / Serwis / Produktywność / Bezpieczeństwo)
2. **Kwota roczna** (input: PLN/rok)
3. **Root Cause** (textarea: min 30 znaków, np. "częste awarie pneumatyki")
4. **Solution Feature** (dropdown: Track & Trace / REDLINK / ONE-KEY / 5-letnia gwarancja / Ergonomia)
5. **Measurable Outcome** (input: np. "-70% downtime, +15% produktywność")
6. **Case Study Reference** (dropdown: VW Poznań / Mahle Krotoszyn / KGHM / Custom)
7. **ROI Number** (input: np. "470% ROI" lub "500k PLN")
8. **Timeframe** (dropdown: 6 miesięcy / 1 rok / 3 lata)
9. **Proposed Action** (dropdown: 2-tygodniowy pilot / Kalkulacja ROI / Spotkanie z CFO / Demo na linii)

**Live Preview**:
- Auto-generuje pitch w real-time
- Character count: "X/150 znaków" (max 150 dla elevator pitch)
- Read time: "~25 sekund"

**Przykład output**:
"Widzę, że **downtime** kosztuje Was **216 000 PLN rocznie** przez **częste awarie pneumatyki**.

Milwaukee rozwiązuje to przez **Track & Trace + REDLINK**, co daje **-70% downtime, +15% produktywność**.

Na podstawie podobnego klienta **VW Poznań**, zaoszczędziliście **470% ROI** w ciągu **3 lata**.

Czy moglibyśmy zmierzyć Wasze savings przez **2-tygodniowy pilot**?"

**Validation**:
- Wszystkie 9 pól wypełnione
- Pitch ≤150 znaków
- Auto-save
- "Zapisz pitch" → +15 XP

**Bonus**:
- "🎤 Nagraj swój pitch" button (mockup - w produkcji: audio recording)
- "📧 Wyślij pitch emailem" (mockup - w produkcji: email template)

---

### **KARTA 10: Summary & Badge** (10 XP)
**Typ**: Summary + Badge popup

**Treść**:

**Gratulacje Header**:
"🎉 Ukończyłeś Value Selling! Teraz umiesz sprzedawać ROI, nie cenę."

**Learning Checklist** (8 punktów):
- ✅ Rozumiem różnicę między ceną a TCO (3-letni całkowity koszt)
- ✅ Potrafię policzyć ROI i payback period dla klienta
- ✅ Znam framework Value Proposition Canvas (pains → gains)
- ✅ Wiem jak przeprowadzić case study conversation (VW Poznań)
- ✅ Umiem odpowiedzieć na 6 klasycznych obiekcji ("za drogo", "nie mamy budżetu")
- ✅ Potrafię zbudować competitive positioning matrix (Milwaukee vs. rynek)
- ✅ Mam gotowy elevator pitch (30 sekund, ROI-focused)
- ✅ Znam strategię bypass Procurement → sell to CFO

**Stats Grid**:
- **XP zdobyte**: [dynamic]
- **Karty ukończone**: 10/10
- **Czas nauki**: ~70 min
- **ROI calculators saved**: [tracked]

**CTA**:
"Gotowy na kolejny krok?"
- Lekcja 3: **Negotiations - Zamykanie trudnych dealów** 🔒 (wkrótce)

**Badge Button**:
"🏆 Pokaż mój badge!"

**Badge Popup**:
- Icon: 💰
- Title: **Value Architect**
- Subtitle: "Milwaukee B2B Academy - Value Selling Master"
- Stats: XP + 10/10 kart
- Message: "Ukończyłeś Value Selling - ROI & TCO. Potrafisz kwantyfikować wartość i sprzedawać business case zamiast narzędzi. **CFO Cię pokocha!**"

**+10 XP completion bonus**

---

## 🎯 Learning Outcomes

Po ukończeniu Lekcji 2 KAM będzie umiał:

1. **Kwantyfikować wartość**:
   - Policzyć TCO 3-letni (nie tylko cena zakupu)
   - Obliczyć ROI, payback period, NPV
   - Zmierzyć savings (downtime, serwis, rotacja, produktywność)

2. **Budować business case**:
   - Stworzyć ROI calculator z danymi klienta
   - Zaprezentować value proposition (pains → gains)
   - Dowieść wartości przez case study (VW, Mahle)

3. **Sprzedawać do CFO**:
   - Bypass Procurement (cena) → sell to CFO (ROI)
   - Używać języka finansów (NPV, IRR, payback)
   - Proponować leasing jako OpEx (nie CapEx)

4. **Obiekcje**:
   - Odpowiadać na "za drogo" kalkulacją TCO
   - Proponować pilot jako proof (no-risk)
   - Konkurencja: value comparison (nie price war)

5. **Pitch**:
   - 30-sekundowy elevator pitch z ROI
   - Positioning Milwaukee vs. konkurencja
   - Call-to-action (pilot, meeting CFO, ROI workshop)

---

## 💾 Technical Notes

**Podobna struktura do Lesson 1**:
- 10 kart, ~70 min, 95 XP
- Mix: Video (1), Prezentacja (1), Interaktywne (6), Quiz (1), Summary (1)
- LocalStorage auto-save
- Mobile responsive
- Badge system

**Nowe komponenty**:
- **ROI Calculator**: Live calculation z 10 inputami + charts
- **Value Proposition Canvas**: 6 textareas (3 pains + 3 gains)
- **Competitive Matrix**: 12×4 tabela z dropdowns + auto-scoring
- **Elevator Pitch Builder**: Mad Libs style z live preview
- **Flashcards**: 6 obiekcji (nie 8 jak w L1)

**Interakcje**:
- Auto-calculation w kalkulatorze (onChange)
- Live character count w pitch builderze
- Progress tracking we flashcards (0/6)
- PDF export mockupy (ROI report, competitive matrix)

**Reuse z Lesson 1**:
- CSS styling (Milwaukee branding)
- Navigation system (prev/next + arrows)
- XP tracking (completedCards Set)
- Badge overlay
- Progress bar

---

## 🚀 Next Steps

Gotowy do budowy HTML mockupu? Powiedz:
- **"Opcja A"** - Zacznij od Etapu 1 (fundament + Card 1)
- **"Full build"** - Zbuduj wszystkie 10 kart od razu (szybciej ale dłuższy output)
- **"Zmień design"** - Chcesz modyfikować karty przed implementacją

Albo: "Najpierw zróbmy Lesson 3 design" (Negotiations) i potem zdecydujemy co budować.

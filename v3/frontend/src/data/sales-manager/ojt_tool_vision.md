# Wizja Produktowa: "OJT Live Coaching Tool"
*Od szkolenia o procesie do prowadzenia procesu.*

## 🎯 Core Philosophy
**"Mniej teorii, więcej narzędzi."**
Zamiast uczyć menedżera, jak wygląda model Feedbacku, aplikacja **generuje** ten feedback na podstawie faktów, które menedżer tylko "wklikuje". Aplikacja jest GPS-em, menedżer jest kierowcą.

---

## 🛠️ The Toolkit (Kluczowe Funkcje)

### 0. Faza 0: Diagnoza i Profilowanie (Setup - Raz na kwartał)
*   **Feature: "The Worker Profile"**
    *   **Cel:** Zrozumienie *jak* dany pracownik się uczy, zanim w ogóle wyjdziemy w teren.
    *   **Komponenty:**
        *   **Styl Uczenia się (Kolb/Honey-Mumford):** Szybki test w appce. Wynik: "Teoretyk", "Aktywista" itd.
        *   **Matryca Kompetencji:** Historia ocen z poprzednich OJT.
    *   **Impact:** Aplikacja personalizuje podpowiedzi. Np. dla "Teoretyka" podpowiada menedżerowi: *"Najpierw wyjaśnij TEORIĘ (dlaczego?), zanim każesz mu to zrobić."*

### 1. Faza Kontraktu (Dzień Przed)
*   **Feature: "Smart Contract Generator"**
    *   **Problem:** Menedżerowie nie wiedzą, jak zacząć / boją się wyjść na "inspektorów".
    *   **Rozwiązanie:** Lista checkboxów (np. "Będę cieniem", "Interweniuję tylko przy ryzyku utraty klienta", "Feedback na koniec dnia").
    *   **Output:** Gotowy SMS/Email do handlowca: *"Cześć! Jutro ruszamy w teren. Umówmy się, że..."*

### 2. Faza Kalibracji (Rano)
*   **Feature: "The Mirror" (Autodiagnoza Krugera-Dunninga)**
    *   **Mechanizm:** Szybki suwak 1-10 dla Menedżera i Handlowca na temat wybranej kompetencji (np. Zamykanie Sprzedaży).
    *   **Logika:** Jeśli Handlowiec daje 9/10, a Menedżer 4/10 -> **ALERT:** *"Wysokie ryzyko oporu. Zacznij feedback od pytań o jego perspektywę."*
*   **Feature: "Situational Leadership Navigator"**
    *   **Test:** 2 pytania: "Umie?" (Tak/Nie) + "Chce?" (Tak/Nie).
    *   **Output:** Aplikacja blokuje/sugeruje styl. Np. dla R4 blokuje "Instruowanie", sugeruje "Delegowanie".

### 3. Faza Odprawy (15 min przed wizytą)
*   **Feature: "Goal Picker"**
    *   **UX:** Karuzela kart ("Badanie Potrzeb", "Obiekcje", "Zamykanie").
    *   **Akcja:** Klikasz jeden cel. Aplikacja: *"Ok, skupiamy się tylko na tym. Zapytaj handlowca: Jak konkretnie chcesz to przećwiczyć?"*

### 4. Faza Wizyty (U klienta)
*   **UX Challenge: "Ból Notowania"**
    *   **Zasada:** Telefon jest w kieszeni/teczce podczas rozmowy. Wyciągamy go tylko w PRZERWACH (toaleta, chwila, gdy klient wychodzi, lub zaraz po wyjściu).
*   **Feature: "Live Observation Pad"**
    *   **Interfejs:** Ciemny ekran, duże przyciski.
    *   **[+] ZACHOWANIE:** Nagraj notatkę głosową (fakt).
    *   **[-] REAKCJA KLIENTA:** Nagraj notatkę głosową.
    *   Aplikacja automatycznie transkrybuje i taguje to jako "Fakt do analizy".

### 5. Faza Analizy (Po wizycie)
*   **Feature: "Feedback Builder"**
    *   **Input:** Algorytm pyta: "Jak poszło?".
    *   **Proces:**
        *   Menedżer: "Słabo".
        *   Appka: "Podaj jeden fakt z Observation Pad".
        *   Menedżer wybiera notatkę głosową nr 2.
        *   Appka: "Wybierz model: FUKO".
    *   **Output:** Gotowy skrypt rozmowy: *"Zauważyłem, że [Fakt]. Spowodowało to [Konsekwencja]. Czego potrzebujesz, żeby...?"*

### 6. Safety Net (Zawsze dostępne)
*   **Feature: "The Question Bank"**
    *   **Widget:** Pływający przycisk "?".
    *   **Działanie:** Utknąłeś? Klikasz i dostajesz "Pytanie-Wytrych" (np. *"Co byś zrobił inaczej, gdybyś miał jeszcze jedną szansę?"*).

---

## 🗺️ User Journey: Dzień z życia Marka (Menedżera)
*Cel: 5 wizyt z Tomkiem (R1 - Początkujący Entuzjasta)*

### 08:00 - Kawa i Kalibracja
Marek otwiera appkę.
1.  **"The Mirror":** Oceniają "Badanie Potrzeb". Tomek daje sobie 8, Marek daje mu 3.
2.  **Appka:** *"Uwaga, efekt Dunninga-Krugera. Tomek nie widzi swoich błędów. Ustalcie cel: Uświadomienie braków."*

### 08:30 - Wizyta 1 (Obserwacja)
Marek chowa telefon. Obserwuje. Tomek zagaduje klienta na śmierć.
Po wyjściu, w samochodzie:
1.  Marek otwiera **"Observation Pad"**.
2.  Nagram notatkę: *"Klient 3 razy patrzył na zegarek, gdy Tomek opowiadał o historii firmy."*

### 10:00 - Wizyta 2 (Trening)
Przed wejściem:
1.  **"Goal Picker":** Marek wybiera "Zadawanie Pytań".
2.  Appka podpowiada: *"Jesteś z R1. Daj mu konkretną instrukcję: 'Zadaj min. 3 pytania otwarte'."*

### 12:00 - Lunch (Feedback Builder)
Marek klika "Podsumuj poranek".
1.  Appka zaciąga fakty z wizyt 1 i 2.
2.  Generuje Feedback (Model Kanapki dla R1):
    *   *"Tomek, super energia (Plus)."*
    *   *"Zauważyłem, że klient patrzył na zegarek (Minus/Fakt)."*
    *   *"W kolejnych wizytach skupmy się tylko na pytaniach (Cel)."*

### 16:00 - Koniec Dnia (Raport)
Aplikacja wysyła do Marka i Tomka podsumowanie dnia z jednym zadaniem domowym.
HR otrzymuje sygnał: "OJT zrealizowane. Poziom kompetencji Tomka w obszarze X wzrósł."

---

## 🚀 Next Steps
1.  Aktualizacja `Lesson 4.3` - `4.7` w planie lekcji, aby odzwierciedlały ten proces (to będą tutoriale do tych narzędzi).
2.  Prototypowanie interfejsu "Goal Picker" i "Observation Pad" w React.

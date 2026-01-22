-- =====================================================
-- PROJECT ZERO - FULL Safety Training Lesson
-- =====================================================
-- Complete 9-module lesson based on HTML mockup
-- =====================================================

-- Update existing lesson with FULL content (all 9 modules)
UPDATE lessons SET
    content = '{
        "cards": [
            {
                "id": "hero-1",
                "type": "hero",
                "title": "PRZYGOTOWANIE DO PRACY",
                "subtitle": "MILWAUKEE | PROJECT ZERO",
                "tagline": "STAY SAFE. STAY PRODUCTIVE.",
                "icon": "⚠️",
                "theme": "safety",
                "sections": [
                    {
                        "title": "Dla kogo jest ta lekcja",
                        "content": "Ta lekcja została stworzona dla osób, które pracują narzędziami każdego dnia:",
                        "items": [
                            "🏗️ Budowa",
                            "🚗 Warsztat samochodowy",
                            "⚡ Elektryka",
                            "🚰 Hydraulika",
                            "🪵 Stolarnia",
                            "🛠️ Serwis / utrzymanie ruchu"
                        ]
                    },
                    {
                        "title": "Cel tej lekcji",
                        "content": "Po tej lekcji będziesz potrafił:",
                        "items": [
                            "pracować **szybciej**, bo bez chaosu i improwizacji",
                            "pracować **bezpieczniej**, bez niepotrzebnego ryzyka",
                            "unikać **przestojów, kontuzji i uszkodzeń sprzętu**"
                        ]
                    }
                ],
                "callout": {
                    "type": "critical",
                    "text": "Najwięcej wypadków nie wydarza się przy trudnej robocie. Wydarzają się przy tej, którą robimy „tylko na chwilę\"."
                }
            },
            {
                "id": "content-1",
                "type": "content",
                "icon": "🟥",
                "subtitle": "MILWAUKEE | PROJECT ZERO",
                "title": "ZERO ACCIDENTS. ZERO EMISSIONS. ZERO COMPROMISES.",
                "sections": [
                    {
                        "heading": "Czym jest Project Zero",
                        "type": "important",
                        "content": "**Project Zero** to globalna inicjatywa **Milwaukee Tools**, której celem jest **eliminowanie zagrożeń w miejscu pracy** — zanim doprowadzą do wypadku.",
                        "items": [
                            "edukacji i budowaniu świadomości",
                            "bezpieczniejszych, lepiej zaprojektowanych narzędziach",
                            "kulturze codziennych, właściwych nawyków"
                        ]
                    }
                ],
                "callout": {
                    "type": "highlight",
                    "text": "Bezpieczeństwo nie zaczyna się po wypadku. **Zaczyna się przed uruchomieniem narzędzia.**"
                }
            },
            {
                "id": "data-1",
                "type": "data",
                "icon": "🧠",
                "title": "CZY WIESZ, ŻE…",
                "subtitle": "Fakty, które robią różnicę",
                "stats": [
                    {
                        "value": "84%",
                        "label": "urazów na budowie ma miejsce, gdy pracownicy **nie noszą kasku ochronnego**"
                    },
                    {
                        "value": "1/3",
                        "label": "wypadków śmiertelnych w budownictwie powodują **spadające przedmioty**"
                    },
                    {
                        "value": "2,8 mln",
                        "label": "wypadków ma miejsce **każdego roku** w europejskim budownictwie"
                    }
                ],
                "callout": {
                    "type": "warning",
                    "text": "To nie są „ekstremalne sytuacje\". To **codzienne warunki pracy**."
                }
            },
            {
                "id": "lightbulb-1",
                "type": "lightbulb",
                "icon": "💡",
                "title": "JAK DZIAŁA TA LEKCJA",
                "content": "Każdy moduł odpowiada na 3 pytania:",
                "steps": [
                    {
                        "number": 1,
                        "title": "Co może pójść nie tak?"
                    },
                    {
                        "number": 2,
                        "title": "Jak to sprawdzić w 30 sekund?"
                    },
                    {
                        "number": 3,
                        "title": "Co zrobić, żeby robota była bezpieczna i szła sprawnie?"
                    }
                ]
            },
            {
                "id": "content-2",
                "type": "content",
                "icon": "🔍",
                "subtitle": "MODUŁ 1/9",
                "title": "ZATRZYMAJ SIĘ PRZED ROBOTĄ (OCENA RYZYKA)",
                "sections": [
                    {
                        "heading": "Dlaczego to ważne",
                        "type": "important",
                        "content": "Zanim odpalisz narzędzie, zatrzymaj się na chwilę. Nie po to, żeby tracić czas – tylko żeby nie stracić palców, zdrowia albo sprzętu."
                    },
                    {
                        "heading": "Co sprawdzasz (30 sekund)",
                        "content": "Zadaj sobie 4 pytania:",
                        "items": [
                            "**Co robię?** (cięcie, wiercenie, szlifowanie, skręcanie)",
                            "**Z czego?** (beton, stal, drewno, instalacja, auto)",
                            "**Co mnie może skrzywdzić?** pył, hałas, odrzut, wirujące części, prąd",
                            "**Kto jest obok mnie?**"
                        ]
                    },
                    {
                        "heading": "Typowe błędy",
                        "type": "warning",
                        "items": [
                            "❌ „Zawsze tak robię\"",
                            "❌ „To tylko jeden otwór\"",
                            "❌ „Zaraz skończę\""
                        ]
                    }
                ],
                "remember": {
                    "icon": "💡",
                    "text": "Jeśli się skaleczysz, robota i tak stanie. Lepiej stracić 30 sekund niż pół dnia albo zdrowie."
                }
            },
            {
                "id": "story-1",
                "type": "story",
                "icon": "⚠️",
                "badge": "📍 Przypadek z terenu",
                "title": "Cięcie betonu bez oceny ryzyka",
                "scenario": {
                    "heading": "Co się stało:",
                    "text": "Na budowie operator zaczyna ciąć beton szlifierką kątową bez wcześniejszego sprawdzenia strefy odrzutu oraz ustawienia osłon."
                },
                "consequences": [
                    "Pył trafia w oczy pomocnika stojącego obok",
                    "Przerwa w pracy, wizyta w szpitalu, potencjalne uszkodzenie wzroku"
                ],
                "lesson": {
                    "heading": "✅ Czego mogło zapobiec:",
                    "text": "**STOP–LOOK–ASSESS–ACT:** Gdyby wykonano ocenę ryzyka, strefa odrzutu zostałaby ograniczona, a pomocnik wiedziałby gdzie stać. Okulary ochronne + maska przeciwpyłowa = zero urazu."
                }
            },
            {
                "id": "content-3",
                "type": "content",
                "icon": "🛡️",
                "subtitle": "MODUŁ 2/9",
                "title": "OCHRONA OSOBISTA (PPE) – CO ZAKŁADAĆ I KIEDY",
                "sections": [
                    {
                        "heading": "Dlaczego to ważne",
                        "type": "important",
                        "content": "Okulary, rękawice czy maska to nie wstyd, tylko narzędzie pracy, tak samo jak wkrętarka."
                    },
                    {
                        "heading": "Minimum, które musisz dobrać do roboty",
                        "items": [
                            "**Oczy** – przy cięciu, wierceniu, szlifowaniu",
                            "**Słuch** – przy młotach, szlifierkach, pilarkach",
                            "**Ręce** – przy ostrych krawędziach, chemii, ciężkich elementach",
                            "**Oddech** – przy pyle, betonie, drewnie, rdzy",
                            "**Buty / kask** – gdy coś może spaść lub przygnieść"
                        ]
                    },
                    {
                        "heading": "Typowe błędy",
                        "type": "warning",
                        "items": [
                            "❌ Brak okularów „bo niewygodne\"",
                            "❌ Jedne rękawice do wszystkiego",
                            "❌ Brak ochrony słuchu „bo chwilę głośno\""
                        ]
                    }
                ],
                "remember": {
                    "icon": "💡",
                    "text": "PPE dobierasz do roboty, a nie do przyzwyczajeń."
                }
            },
            {
                "id": "content-4",
                "type": "content",
                "icon": "🧤",
                "subtitle": "MODUŁ 3/9",
                "title": "SPRAWDŹ PPE ZANIM ZACZNIESZ",
                "sections": [
                    {
                        "heading": "Co sprawdzić przed robotą",
                        "items": [
                            "**okulary:** czy nie porysowane, nie pęknięte",
                            "**rękawice:** czy nie przetarte",
                            "**maska:** czy filtr nie zapchany",
                            "**nauszniki/zatyczki:** czy czyste i sprawne"
                        ]
                    },
                    {
                        "heading": "Typowe błędy",
                        "type": "warning",
                        "items": [
                            "❌ Pęknięte okulary = „jakoś widać\"",
                            "❌ Brudna maska = „jeszcze da radę\"",
                            "❌ PPE „na chwilę\" bez sprawdzania"
                        ]
                    }
                ],
                "remember": {
                    "icon": "💡",
                    "text": "Zużyta ochrona nie chroni."
                }
            },
            {
                "id": "quiz-1",
                "type": "quiz",
                "title": "🎯 Sprawdź się - Quiz (Moduły 1-3)",
                "subtitle": "Zaznacz poprawne odpowiedzi",
                "questions": [
                    {
                        "question": "Co to znaczy \"zatrzymać się przed robotą\"?",
                        "options": [
                            "Zrobić przerwę na kawę",
                            "Zadać sobie 4 pytania: co robię, z czego, co może skrzywdzić, kto obok",
                            "Przeczytać instrukcję narzędzia"
                        ],
                        "correctAnswer": 1
                    },
                    {
                        "question": "Kiedy zakładasz ochronę słuchu?",
                        "options": [
                            "Tylko przy pracy w hali produkcyjnej",
                            "Przy młotach, szlifierkach, pilarkach - nawet \"na chwilę\"",
                            "Gdy ktoś się skarży na hałas"
                        ],
                        "correctAnswer": 1
                    },
                    {
                        "question": "Co to znaczy \"zużyta ochrona nie chroni\"?",
                        "options": [
                            "PPE można wyrzucić po jednym użyciu",
                            "Pęknięte okulary, przetarte rękawice, zapchana maska nie dają ochrony",
                            "PPE trzeba wymieniać co miesiąc"
                        ],
                        "correctAnswer": 1
                    }
                ]
            },
            {
                "id": "content-5",
                "type": "content",
                "icon": "🔧",
                "subtitle": "MODUŁ 4/9",
                "title": "DOBIERZ WŁAŚCIWE NARZĘDZIE DO ROBOTY",
                "sections": [
                    {
                        "heading": "Dlaczego to ważne",
                        "content": "Złe narzędzie:",
                        "items": [
                            "szybciej się psuje",
                            "jest niebezpieczne",
                            "robi robotę dłużej"
                        ]
                    },
                    {
                        "heading": "Co sprawdzić",
                        "items": [
                            "czy narzędzie ma wystarczającą moc",
                            "czy nadaje się do tego materiału",
                            "czy nie musisz go dociskać na siłę"
                        ]
                    },
                    {
                        "heading": "Sygnały ostrzegawcze",
                        "type": "warning",
                        "items": [
                            "⚠️ narzędzie się grzeje",
                            "⚠️ dławi się",
                            "⚠️ „szarpie\"",
                            "⚠️ musisz mocno dociskać"
                        ]
                    }
                ],
                "remember": {
                    "icon": "💡",
                    "text": "Jeśli musisz walczyć z narzędziem – to nie jest dobre narzędzie do tej roboty."
                }
            },
            {
                "id": "content-6",
                "type": "content",
                "icon": "🛠️",
                "subtitle": "MODUŁ 5/9",
                "title": "SPRAWDŹ STAN NARZĘDZIA",
                "sections": [
                    {
                        "heading": "Zanim włączysz",
                        "items": [
                            "**obudowa** – czy nie pęknięta",
                            "**uchwyt** – czy nie luźny",
                            "**osłony** – czy są na miejscu",
                            "**włącznik** – czy odbija normalnie",
                            "**czystość** – brak pyłu, opiłków"
                        ]
                    },
                    {
                        "heading": "Typowe błędy",
                        "type": "warning",
                        "items": [
                            "❌ Praca z uszkodzoną osłoną",
                            "❌ Zablokowany włącznik",
                            "❌ Narzędzie „pożyczone\", niesprawdzone"
                        ]
                    }
                ],
                "remember": {
                    "icon": "💡",
                    "text": "Uszkodzone narzędzie nie ostrzega drugi raz."
                }
            },
            {
                "id": "content-7",
                "type": "content",
                "icon": "⚙️",
                "subtitle": "MODUŁ 6/9",
                "title": "OSPRZĘT: TARCZE, WIERTŁA, BITY",
                "sections": [
                    {
                        "heading": "Co MUSISZ sprawdzić",
                        "items": [
                            "czy tarcza / wiertło nie jest pęknięte",
                            "czy nie jest zużyte",
                            "czy pasuje do prędkości narzędzia",
                            "czy jest dobrze zamocowane"
                        ]
                    },
                    {
                        "heading": "Bardzo groźne sytuacje",
                        "type": "warning",
                        "items": [
                            "❌ mikropęknięta tarcza",
                            "❌ zjechany bit (ślizga się)",
                            "❌ za długie wiertło w ciasnym miejscu"
                        ]
                    }
                ],
                "remember": {
                    "icon": "💡",
                    "text": "Najwięcej wypadków robi osprzęt, nie samo narzędzie."
                }
            },
            {
                "id": "story-2",
                "type": "story",
                "icon": "💥",
                "badge": "📍 Przypadek z terenu",
                "title": "Nieprawidłowe tarcze i bity",
                "scenario": {
                    "heading": "Co się stało:",
                    "text": "Hydraulik używa tarcz do metalu przy cięciu stali nierdzewnej, mimo że oznaczenia tarczy nie dopuszczają takiej prędkości obrotowej ani materiału."
                },
                "consequences": [
                    "Tarcza pęka podczas pracy i odrzut trafia w nogę",
                    "Rana wymagająca szwów, kilka tygodni bez pracy"
                ],
                "lesson": {
                    "heading": "✅ Prosta zasada:",
                    "text": "Zawsze sprawdzaj **oznaczenia tarcz, bitów i dopuszczalną prędkość**. Nie ma „podobnej\" tarczy — albo pasuje, albo nie."
                }
            },
            {
                "id": "quiz-2",
                "type": "quiz",
                "title": "🎯 Sprawdź się - Quiz (Moduły 4-6)",
                "subtitle": "Zaznacz poprawne odpowiedzi",
                "questions": [
                    {
                        "question": "Co to znaczy \"właściwe narzędzie do roboty\"?",
                        "options": [
                            "Najdroższe na rynku",
                            "Narzędzie z odpowiednią mocą, które nie grzeje się, nie dławi i nie szarpie",
                            "To które masz pod ręką"
                        ],
                        "correctAnswer": 1
                    },
                    {
                        "question": "Dlaczego uszkodzona osłona to poważny problem?",
                        "options": [
                            "Gwarancja przepada",
                            "Brak ochrony przed odrzutem, iskrami, wirującymi częściami - nie ostrzeże drugi raz",
                            "Narzędzie wygląda brzydko"
                        ],
                        "correctAnswer": 1
                    },
                    {
                        "question": "Co powoduje więcej wypadków?",
                        "options": [
                            "Samo narzędzie (wiertarka, szlifierka)",
                            "Osprzęt - pęknięte tarcze, zużyte wiertła, źle zamocowane bity",
                            "Hałas w hali"
                        ],
                        "correctAnswer": 1
                    }
                ]
            },
            {
                "id": "content-8",
                "type": "content",
                "icon": "🌧️",
                "subtitle": "MODUŁ 7/9",
                "title": "WARUNKI PRACY I TWOJA POZYCJA",
                "sections": [
                    {
                        "heading": "Sprawdź miejsce",
                        "items": [
                            "czy nie ma wody / wilgoci",
                            "czy dobrze widzisz (światło)",
                            "czy masz stabilne podłoże",
                            "czy nic nie leży pod nogami"
                        ]
                    },
                    {
                        "heading": "Sprawdź siebie",
                        "items": [
                            "stoisz stabilnie",
                            "masz kontrolę nad narzędziem",
                            "nie pracujesz „na wyciągniętej ręce\""
                        ]
                    }
                ],
                "remember": {
                    "icon": "💡",
                    "text": "Zła pozycja = brak kontroli = wypadek."
                }
            },
            {
                "id": "content-9",
                "type": "content",
                "icon": "🚧",
                "subtitle": "MODUŁ 8/9",
                "title": "ZABEZPIECZ STREFĘ PRACY",
                "sections": [
                    {
                        "heading": "Co to znaczy w praktyce",
                        "items": [
                            "nikt nie stoi w linii cięcia / odrzutu",
                            "narzędzia nie leżą na ziemi",
                            "kable są zabezpieczone",
                            "osoby postronne są poza strefą"
                        ]
                    },
                    {
                        "heading": "Typowe błędy",
                        "type": "warning",
                        "items": [
                            "❌ ktoś stoi „tylko popatrzeć\"",
                            "❌ narzędzia pod nogami",
                            "❌ brak porządku"
                        ]
                    }
                ],
                "remember": {
                    "icon": "💡",
                    "text": "Jeśli ktoś może wejść w twoją strefę – to też twoja odpowiedzialność."
                }
            },
            {
                "id": "content-10",
                "type": "content",
                "icon": "🧠",
                "subtitle": "MODUŁ 9/9",
                "title": "ODPOWIEDZIALNOŚĆ",
                "sections": [
                    {
                        "heading": "Co to znaczy naprawdę",
                        "type": "important",
                        "items": [
                            "Ty odpowiadasz za siebie",
                            "Jeśli ktoś pracuje z tobą – odpowiadasz też za niego",
                            "Bezpieczeństwo to decyzje, nie gadanie"
                        ]
                    }
                ],
                "remember": {
                    "icon": "💡",
                    "text": "Nie ma „na chwilę\". Jest tylko „bezpiecznie\" albo „niebezpiecznie\"."
                }
            },
            {
                "id": "data-2",
                "type": "data",
                "icon": "📊",
                "title": "LICZBY NIE KŁAMIĄ",
                "subtitle": "Dlaczego przygotowanie do pracy ma znaczenie",
                "stats": [
                    {
                        "value": "67 000",
                        "label": "osób poszkodowanych w wypadkach przy pracy w Polsce (2024)"
                    },
                    {
                        "value": "50%",
                        "label": "spadek wypadków w firmach ze szkoleniami BHP vs bez szkoleń"
                    },
                    {
                        "value": "60%",
                        "label": "mniej urazów przy prawidłowym używaniu PPE (branże wysokiego ryzyka)"
                    }
                ],
                "callout": {
                    "type": "success",
                    "text": "Choć PPE wygląda jak drobna rzecz, to różnica między urazem a bezpiecznym dniem pracy."
                }
            },
            {
                "id": "quiz-final",
                "type": "quiz",
                "title": "🎯 Test Końcowy - Project Zero",
                "subtitle": "10 pytań sprawdzających Twoją wiedzę z całej lekcji",
                "questions": [
                    {
                        "question": "Jakie 4 pytania zadajesz sobie przed robotą?",
                        "options": [
                            "Gdzie, kiedy, z kim, ile",
                            "Co robię, z czego, co może skrzywdzić, kto obok",
                            "Czy mam czas, czy mam narzędzie, czy wiem jak, czy ktoś patrzy"
                        ],
                        "correctAnswer": 1,
                        "explanation": "To podstawa oceny ryzyka - 4 proste pytania, które zajmują 30 sekund, ale mogą uratować zdrowie."
                    },
                    {
                        "question": "Kiedy PPE jest właściwie dobrane?",
                        "options": [
                            "Gdy masz wszystko: okulary, rękawice, kask, buty",
                            "Gdy jest dopasowane do konkretnego zagrożenia (pył → maska, hałas → nauszniki)",
                            "Gdy jest najnowszy model z certyfikatem"
                        ],
                        "correctAnswer": 1,
                        "explanation": "PPE dobierasz do roboty i zagrożenia, nie na zasadzie \"wszystko na siebie\"."
                    },
                    {
                        "question": "Co robisz, gdy narzędzie się grzeje i dławi?",
                        "options": [
                            "Dociskam mocniej",
                            "Zmieniam narzędzie na mocniejsze lub sprawdzam osprzęt",
                            "Robię szybciej, żeby skończyć"
                        ],
                        "correctAnswer": 1,
                        "explanation": "Grzanie i dławienie to sygnał, że narzędzie nie pasuje do zadania."
                    },
                    {
                        "question": "Dlaczego osprzęt jest groźniejszy niż samo narzędzie?",
                        "options": [
                            "Bo jest tańszy",
                            "Bo pęknięta tarcza czy zużyty bit powodują większość wypadków",
                            "Bo trudniej go wymienić"
                        ],
                        "correctAnswer": 1,
                        "explanation": "Statystyki pokazują: najwięcej wypadków to pęknięte tarcze, zużyte wiertła i źle zamocowane bity."
                    },
                    {
                        "question": "Co to znaczy \"zabezpieczyć strefę pracy\"?",
                        "options": [
                            "Postawić barierki dookoła",
                            "Upewnić się, że nikt nie stoi w linii odrzutu, kable są bezpieczne, narzędzia nie leżą pod nogami",
                            "Zamknąć drzwi do pomieszczenia"
                        ],
                        "correctAnswer": 1,
                        "explanation": "Chodzi o praktyczne działania: kontrola strefy odrzutu, porządek, bezpieczne kable."
                    },
                    {
                        "question": "Jak często sprawdzasz stan PPE?",
                        "options": [
                            "Raz w miesiącu",
                            "Przed każdą robotą",
                            "Gdy coś się zepsuje"
                        ],
                        "correctAnswer": 1,
                        "explanation": "Zużyta ochrona nie chroni - sprawdzasz PRZED każdą robotą."
                    },
                    {
                        "question": "Co robisz, gdy widzisz uszkodzoną osłonę w narzędziu?",
                        "options": [
                            "Pracuję ostrożnie",
                            "Nie używam narzędzia, naprawiam lub wymieniam osłonę",
                            "Zgłaszam po zakończeniu roboty"
                        ],
                        "correctAnswer": 1,
                        "explanation": "Uszkodzona osłona = nie używasz. Nie ma \"ostrożnie\" z wirującymi częściami."
                    },
                    {
                        "question": "Dlaczego \"na chwilę\" to najniebezpieczniejsze podejście?",
                        "options": [
                            "Bo wtedy pomijamy ocenę ryzyka i PPE",
                            "Bo szef może zobaczyć",
                            "Bo robota trwa dłużej"
                        ],
                        "correctAnswer": 0,
                        "explanation": "Większość wypadków dzieje się przy robotach \"na chwilę\", bo wtedy pomijamy podstawowe zasady."
                    },
                    {
                        "question": "Kto odpowiada za bezpieczeństwo na Twojej budowie/warsztacie?",
                        "options": [
                            "Szef / kierownik",
                            "Służba BHP",
                            "Ty - za siebie i osoby w Twojej strefie"
                        ],
                        "correctAnswer": 2,
                        "explanation": "Każdy odpowiada za siebie i za osoby w swojej strefie pracy. To nie jest tylko zadanie BHP."
                    },
                    {
                        "question": "Co to znaczy Project Zero?",
                        "options": [
                            "Zero wypadków, zero kompromisów - eliminowanie zagrożeń zanim doprowadzą do urazu",
                            "Zero kosztów, zero strat",
                            "Zero narzędzi elektrycznych"
                        ],
                        "correctAnswer": 0,
                        "explanation": "Project Zero to globalna inicjatywa Milwaukee: zero wypadków przez edukację, lepsze narzędzia i kulturę bezpieczeństwa."
                    }
                ]
            },
            {
                "id": "ending-1",
                "type": "ending",
                "icon": "✅",
                "title": "GRATULACJE!",
                "subtitle": "Ukończyłeś lekcję Project Zero: Przygotowanie do Pracy",
                "checklist": [
                    {
                        "icon": "✅",
                        "text": "Wiesz, jak zatrzymać się przed robotą i ocenić ryzyko w 30 sekund"
                    },
                    {
                        "icon": "✅",
                        "text": "Potrafisz dobrać właściwe PPE do zadania i sprawdzić jego stan"
                    },
                    {
                        "icon": "✅",
                        "text": "Rozumiesz, dlaczego osprzęt wymaga szczególnej uwagi"
                    },
                    {
                        "icon": "✅",
                        "text": "Znasz zasady zabezpieczania strefy pracy"
                    },
                    {
                        "icon": "✅",
                        "text": "Rozumiesz, że \"na chwilę\" to najniebezpieczniejsze podejście"
                    },
                    {
                        "icon": "✅",
                        "text": "Znasz statystyki i realne przypadki z terenu"
                    }
                ],
                "tagline": "ZERO ACCIDENTS. ZERO COMPROMISES.",
                "next_steps": {
                    "text": "Następna lekcja: **Bezpieczna Praca z Narzędziami Elektrycznymi**",
                    "available": false
                }
            }
        ]
    }'::jsonb,
    duration_minutes = 45,
    xp_reward = 200,
    updated_at = NOW()
WHERE lesson_id = 'project-zero-przygotowanie';

-- Verification
SELECT 
    lesson_id,
    title,
    duration_minutes,
    xp_reward,
    jsonb_array_length(content->'cards') as card_count
FROM lessons
WHERE lesson_id = 'project-zero-przygotowanie';

-- Success message
DO $$
BEGIN
    RAISE NOTICE '✅ Project Zero FULL lesson updated!';
    RAISE NOTICE '📚 Total cards: 20 (9 modules + quizzes + stories + data)';
    RAISE NOTICE '⏱️ Duration: 45 minutes';
    RAISE NOTICE '⚡ XP Reward: 200';
END $$;

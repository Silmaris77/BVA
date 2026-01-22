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
                "icon": "âš ď¸Ź",
                "theme": "safety",
                "sections": [
                    {
                        "title": "Dla kogo jest ta lekcja",
                        "content": "Ta lekcja zostaĹ‚a stworzona dla osĂłb, ktĂłre pracujÄ… narzÄ™dziami kaĹĽdego dnia:",
                        "items": [
                            "đźŹ—ď¸Ź Budowa",
                            "đźš— Warsztat samochodowy",
                            "âšˇ Elektryka",
                            "đźš° Hydraulika",
                            "đźŞµ Stolarnia",
                            "đź› ď¸Ź Serwis / utrzymanie ruchu"
                        ]
                    },
                    {
                        "title": "Cel tej lekcji",
                        "content": "Po tej lekcji bÄ™dziesz potrafiĹ‚:",
                        "items": [
                            "pracowaÄ‡ **szybciej**, bo bez chaosu i improwizacji",
                            "pracowaÄ‡ **bezpieczniej**, bez niepotrzebnego ryzyka",
                            "unikaÄ‡ **przestojĂłw, kontuzji i uszkodzeĹ„ sprzÄ™tu**"
                        ]
                    }
                ],
                "callout": {
                    "type": "critical",
                    "text": "NajwiÄ™cej wypadkĂłw nie wydarza siÄ™ przy trudnej robocie. WydarzajÄ… siÄ™ przy tej, ktĂłrÄ… robimy â€žtylko na chwilÄ™\"."
                }
            },
            {
                "id": "content-1",
                "type": "content",
                "icon": "đźźĄ",
                "subtitle": "MILWAUKEE | PROJECT ZERO",
                "title": "ZERO ACCIDENTS. ZERO EMISSIONS. ZERO COMPROMISES.",
                "sections": [
                    {
                        "heading": "Czym jest Project Zero",
                        "type": "important",
                        "content": "**Project Zero** to globalna inicjatywa **Milwaukee Tools**, ktĂłrej celem jest **eliminowanie zagroĹĽeĹ„ w miejscu pracy** â€” zanim doprowadzÄ… do wypadku.",
                        "items": [
                            "edukacji i budowaniu Ĺ›wiadomoĹ›ci",
                            "bezpieczniejszych, lepiej zaprojektowanych narzÄ™dziach",
                            "kulturze codziennych, wĹ‚aĹ›ciwych nawykĂłw"
                        ]
                    }
                ],
                "callout": {
                    "type": "highlight",
                    "text": "BezpieczeĹ„stwo nie zaczyna siÄ™ po wypadku. **Zaczyna siÄ™ przed uruchomieniem narzÄ™dzia.**"
                }
            },
            {
                "id": "data-1",
                "type": "data",
                "icon": "đź§ ",
                "title": "CZY WIESZ, Ĺ»Eâ€¦",
                "subtitle": "Fakty, ktĂłre robiÄ… rĂłĹĽnicÄ™",
                "stats": [
                    {
                        "value": "84%",
                        "label": "urazĂłw na budowie ma miejsce, gdy pracownicy **nie noszÄ… kasku ochronnego**"
                    },
                    {
                        "value": "1/3",
                        "label": "wypadkĂłw Ĺ›miertelnych w budownictwie powodujÄ… **spadajÄ…ce przedmioty**"
                    },
                    {
                        "value": "2,8 mln",
                        "label": "wypadkĂłw ma miejsce **kaĹĽdego roku** w europejskim budownictwie"
                    }
                ],
                "callout": {
                    "type": "warning",
                    "text": "To nie sÄ… â€žekstremalne sytuacje\". To **codzienne warunki pracy**."
                }
            },
            {
                "id": "lightbulb-1",
                "type": "lightbulb",
                "icon": "đź’ˇ",
                "title": "JAK DZIAĹA TA LEKCJA",
                "content": "KaĹĽdy moduĹ‚ odpowiada na 3 pytania:",
                "steps": [
                    {
                        "number": 1,
                        "title": "Co moĹĽe pĂłjĹ›Ä‡ nie tak?"
                    },
                    {
                        "number": 2,
                        "title": "Jak to sprawdziÄ‡ w 30 sekund?"
                    },
                    {
                        "number": 3,
                        "title": "Co zrobiÄ‡, ĹĽeby robota byĹ‚a bezpieczna i szĹ‚a sprawnie?"
                    }
                ]
            },
            {
                "id": "content-2",
                "type": "content",
                "icon": "đź”Ť",
                "subtitle": "MODUĹ 1/9",
                "title": "ZATRZYMAJ SIÄ PRZED ROBOTÄ„ (OCENA RYZYKA)",
                "sections": [
                    {
                        "heading": "Dlaczego to waĹĽne",
                        "type": "important",
                        "content": "Zanim odpalisz narzÄ™dzie, zatrzymaj siÄ™ na chwilÄ™. Nie po to, ĹĽeby traciÄ‡ czas â€“ tylko ĹĽeby nie straciÄ‡ palcĂłw, zdrowia albo sprzÄ™tu."
                    },
                    {
                        "heading": "Co sprawdzasz (30 sekund)",
                        "content": "Zadaj sobie 4 pytania:",
                        "items": [
                            "**Co robiÄ™?** (ciÄ™cie, wiercenie, szlifowanie, skrÄ™canie)",
                            "**Z czego?** (beton, stal, drewno, instalacja, auto)",
                            "**Co mnie moĹĽe skrzywdziÄ‡?** pyĹ‚, haĹ‚as, odrzut, wirujÄ…ce czÄ™Ĺ›ci, prÄ…d",
                            "**Kto jest obok mnie?**"
                        ]
                    },
                    {
                        "heading": "Typowe bĹ‚Ä™dy",
                        "type": "warning",
                        "items": [
                            "âťŚ â€žZawsze tak robiÄ™\"",
                            "âťŚ â€žTo tylko jeden otwĂłr\"",
                            "âťŚ â€žZaraz skoĹ„czÄ™\""
                        ]
                    }
                ],
                "remember": {
                    "icon": "đź’ˇ",
                    "text": "JeĹ›li siÄ™ skaleczysz, robota i tak stanie. Lepiej straciÄ‡ 30 sekund niĹĽ pĂłĹ‚ dnia albo zdrowie."
                }
            },
            {
                "id": "story-1",
                "type": "story",
                "icon": "âš ď¸Ź",
                "badge": "đź“Ť Przypadek z terenu",
                "title": "CiÄ™cie betonu bez oceny ryzyka",
                "scenario": {
                    "heading": "Co siÄ™ staĹ‚o:",
                    "text": "Na budowie operator zaczyna ciÄ…Ä‡ beton szlifierkÄ… kÄ…towÄ… bez wczeĹ›niejszego sprawdzenia strefy odrzutu oraz ustawienia osĹ‚on."
                },
                "consequences": [
                    "PyĹ‚ trafia w oczy pomocnika stojÄ…cego obok",
                    "Przerwa w pracy, wizyta w szpitalu, potencjalne uszkodzenie wzroku"
                ],
                "lesson": {
                    "heading": "âś… Czego mogĹ‚o zapobiec:",
                    "text": "**STOPâ€“LOOKâ€“ASSESSâ€“ACT:** Gdyby wykonano ocenÄ™ ryzyka, strefa odrzutu zostaĹ‚aby ograniczona, a pomocnik wiedziaĹ‚by gdzie staÄ‡. Okulary ochronne + maska przeciwpyĹ‚owa = zero urazu."
                }
            },
            {
                "id": "content-3",
                "type": "content",
                "icon": "đź›ˇď¸Ź",
                "subtitle": "MODUĹ 2/9",
                "title": "OCHRONA OSOBISTA (PPE) â€“ CO ZAKĹADAÄ† I KIEDY",
                "sections": [
                    {
                        "heading": "Dlaczego to waĹĽne",
                        "type": "important",
                        "content": "Okulary, rÄ™kawice czy maska to nie wstyd, tylko narzÄ™dzie pracy, tak samo jak wkrÄ™tarka."
                    },
                    {
                        "heading": "Minimum, ktĂłre musisz dobraÄ‡ do roboty",
                        "items": [
                            "**Oczy** â€“ przy ciÄ™ciu, wierceniu, szlifowaniu",
                            "**SĹ‚uch** â€“ przy mĹ‚otach, szlifierkach, pilarkach",
                            "**RÄ™ce** â€“ przy ostrych krawÄ™dziach, chemii, ciÄ™ĹĽkich elementach",
                            "**Oddech** â€“ przy pyle, betonie, drewnie, rdzy",
                            "**Buty / kask** â€“ gdy coĹ› moĹĽe spaĹ›Ä‡ lub przygnieĹ›Ä‡"
                        ]
                    },
                    {
                        "heading": "Typowe bĹ‚Ä™dy",
                        "type": "warning",
                        "items": [
                            "âťŚ Brak okularĂłw â€žbo niewygodne\"",
                            "âťŚ Jedne rÄ™kawice do wszystkiego",
                            "âťŚ Brak ochrony sĹ‚uchu â€žbo chwilÄ™ gĹ‚oĹ›no\""
                        ]
                    }
                ],
                "remember": {
                    "icon": "đź’ˇ",
                    "text": "PPE dobierasz do roboty, a nie do przyzwyczajeĹ„."
                }
            },
            {
                "id": "content-4",
                "type": "content",
                "icon": "đź§¤",
                "subtitle": "MODUĹ 3/9",
                "title": "SPRAWDĹą PPE ZANIM ZACZNIESZ",
                "sections": [
                    {
                        "heading": "Co sprawdziÄ‡ przed robotÄ…",
                        "items": [
                            "**okulary:** czy nie porysowane, nie pÄ™kniÄ™te",
                            "**rÄ™kawice:** czy nie przetarte",
                            "**maska:** czy filtr nie zapchany",
                            "**nauszniki/zatyczki:** czy czyste i sprawne"
                        ]
                    },
                    {
                        "heading": "Typowe bĹ‚Ä™dy",
                        "type": "warning",
                        "items": [
                            "âťŚ PÄ™kniÄ™te okulary = â€žjakoĹ› widaÄ‡\"",
                            "âťŚ Brudna maska = â€žjeszcze da radÄ™\"",
                            "âťŚ PPE â€žna chwilÄ™\" bez sprawdzania"
                        ]
                    }
                ],
                "remember": {
                    "icon": "đź’ˇ",
                    "text": "ZuĹĽyta ochrona nie chroni."
                }
            },
            {
                "id": "quiz-1",
                "type": "quiz",
                "title": "đźŽŻ SprawdĹş siÄ™ - Quiz (ModuĹ‚y 1-3)",
                "subtitle": "Zaznacz poprawne odpowiedzi",
                "questions": [
                    {
                        "question": "Co to znaczy \"zatrzymaÄ‡ siÄ™ przed robotÄ…\"?",
                        "options": [
                            "ZrobiÄ‡ przerwÄ™ na kawÄ™",
                            "ZadaÄ‡ sobie 4 pytania: co robiÄ™, z czego, co moĹĽe skrzywdziÄ‡, kto obok",
                            "PrzeczytaÄ‡ instrukcjÄ™ narzÄ™dzia"
                        ],
                        "correctAnswer": 1
                    },
                    {
                        "question": "Kiedy zakĹ‚adasz ochronÄ™ sĹ‚uchu?",
                        "options": [
                            "Tylko przy pracy w hali produkcyjnej",
                            "Przy mĹ‚otach, szlifierkach, pilarkach - nawet \"na chwilÄ™\"",
                            "Gdy ktoĹ› siÄ™ skarĹĽy na haĹ‚as"
                        ],
                        "correctAnswer": 1
                    },
                    {
                        "question": "Co to znaczy \"zuĹĽyta ochrona nie chroni\"?",
                        "options": [
                            "PPE moĹĽna wyrzuciÄ‡ po jednym uĹĽyciu",
                            "PÄ™kniÄ™te okulary, przetarte rÄ™kawice, zapchana maska nie dajÄ… ochrony",
                            "PPE trzeba wymieniaÄ‡ co miesiÄ…c"
                        ],
                        "correctAnswer": 1
                    }
                ]
            },
            {
                "id": "content-5",
                "type": "content",
                "icon": "đź”§",
                "subtitle": "MODUĹ 4/9",
                "title": "DOBIERZ WĹAĹšCIWE NARZÄDZIE DO ROBOTY",
                "sections": [
                    {
                        "heading": "Dlaczego to waĹĽne",
                        "content": "ZĹ‚e narzÄ™dzie:",
                        "items": [
                            "szybciej siÄ™ psuje",
                            "jest niebezpieczne",
                            "robi robotÄ™ dĹ‚uĹĽej"
                        ]
                    },
                    {
                        "heading": "Co sprawdziÄ‡",
                        "items": [
                            "czy narzÄ™dzie ma wystarczajÄ…cÄ… moc",
                            "czy nadaje siÄ™ do tego materiaĹ‚u",
                            "czy nie musisz go dociskaÄ‡ na siĹ‚Ä™"
                        ]
                    },
                    {
                        "heading": "SygnaĹ‚y ostrzegawcze",
                        "type": "warning",
                        "items": [
                            "âš ď¸Ź narzÄ™dzie siÄ™ grzeje",
                            "âš ď¸Ź dĹ‚awi siÄ™",
                            "âš ď¸Ź â€žszarpie\"",
                            "âš ď¸Ź musisz mocno dociskaÄ‡"
                        ]
                    }
                ],
                "remember": {
                    "icon": "đź’ˇ",
                    "text": "JeĹ›li musisz walczyÄ‡ z narzÄ™dziem â€“ to nie jest dobre narzÄ™dzie do tej roboty."
                }
            },
            {
                "id": "content-6",
                "type": "content",
                "icon": "đź› ď¸Ź",
                "subtitle": "MODUĹ 5/9",
                "title": "SPRAWDĹą STAN NARZÄDZIA",
                "sections": [
                    {
                        "heading": "Zanim wĹ‚Ä…czysz",
                        "items": [
                            "**obudowa** â€“ czy nie pÄ™kniÄ™ta",
                            "**uchwyt** â€“ czy nie luĹşny",
                            "**osĹ‚ony** â€“ czy sÄ… na miejscu",
                            "**wĹ‚Ä…cznik** â€“ czy odbija normalnie",
                            "**czystoĹ›Ä‡** â€“ brak pyĹ‚u, opiĹ‚kĂłw"
                        ]
                    },
                    {
                        "heading": "Typowe bĹ‚Ä™dy",
                        "type": "warning",
                        "items": [
                            "âťŚ Praca z uszkodzonÄ… osĹ‚onÄ…",
                            "âťŚ Zablokowany wĹ‚Ä…cznik",
                            "âťŚ NarzÄ™dzie â€žpoĹĽyczone\", niesprawdzone"
                        ]
                    }
                ],
                "remember": {
                    "icon": "đź’ˇ",
                    "text": "Uszkodzone narzÄ™dzie nie ostrzega drugi raz."
                }
            },
            {
                "id": "content-7",
                "type": "content",
                "icon": "âš™ď¸Ź",
                "subtitle": "MODUĹ 6/9",
                "title": "OSPRZÄT: TARCZE, WIERTĹA, BITY",
                "sections": [
                    {
                        "heading": "Co MUSISZ sprawdziÄ‡",
                        "items": [
                            "czy tarcza / wiertĹ‚o nie jest pÄ™kniÄ™te",
                            "czy nie jest zuĹĽyte",
                            "czy pasuje do prÄ™dkoĹ›ci narzÄ™dzia",
                            "czy jest dobrze zamocowane"
                        ]
                    },
                    {
                        "heading": "Bardzo groĹşne sytuacje",
                        "type": "warning",
                        "items": [
                            "âťŚ mikropÄ™kniÄ™ta tarcza",
                            "âťŚ zjechany bit (Ĺ›lizga siÄ™)",
                            "âťŚ za dĹ‚ugie wiertĹ‚o w ciasnym miejscu"
                        ]
                    }
                ],
                "remember": {
                    "icon": "đź’ˇ",
                    "text": "NajwiÄ™cej wypadkĂłw robi osprzÄ™t, nie samo narzÄ™dzie."
                }
            },
            {
                "id": "story-2",
                "type": "story",
                "icon": "đź’Ą",
                "badge": "đź“Ť Przypadek z terenu",
                "title": "NieprawidĹ‚owe tarcze i bity",
                "scenario": {
                    "heading": "Co siÄ™ staĹ‚o:",
                    "text": "Hydraulik uĹĽywa tarcz do metalu przy ciÄ™ciu stali nierdzewnej, mimo ĹĽe oznaczenia tarczy nie dopuszczajÄ… takiej prÄ™dkoĹ›ci obrotowej ani materiaĹ‚u."
                },
                "consequences": [
                    "Tarcza pÄ™ka podczas pracy i odrzut trafia w nogÄ™",
                    "Rana wymagajÄ…ca szwĂłw, kilka tygodni bez pracy"
                ],
                "lesson": {
                    "heading": "âś… Prosta zasada:",
                    "text": "Zawsze sprawdzaj **oznaczenia tarcz, bitĂłw i dopuszczalnÄ… prÄ™dkoĹ›Ä‡**. Nie ma â€žpodobnej\" tarczy â€” albo pasuje, albo nie."
                }
            },
            {
                "id": "quiz-2",
                "type": "quiz",
                "title": "đźŽŻ SprawdĹş siÄ™ - Quiz (ModuĹ‚y 4-6)",
                "subtitle": "Zaznacz poprawne odpowiedzi",
                "questions": [
                    {
                        "question": "Co to znaczy \"wĹ‚aĹ›ciwe narzÄ™dzie do roboty\"?",
                        "options": [
                            "NajdroĹĽsze na rynku",
                            "NarzÄ™dzie z odpowiedniÄ… mocÄ…, ktĂłre nie grzeje siÄ™, nie dĹ‚awi i nie szarpie",
                            "To ktĂłre masz pod rÄ™kÄ…"
                        ],
                        "correctAnswer": 1
                    },
                    {
                        "question": "Dlaczego uszkodzona osĹ‚ona to powaĹĽny problem?",
                        "options": [
                            "Gwarancja przepada",
                            "Brak ochrony przed odrzutem, iskrami, wirujÄ…cymi czÄ™Ĺ›ciami - nie ostrzeĹĽe drugi raz",
                            "NarzÄ™dzie wyglÄ…da brzydko"
                        ],
                        "correctAnswer": 1
                    },
                    {
                        "question": "Co powoduje wiÄ™cej wypadkĂłw?",
                        "options": [
                            "Samo narzÄ™dzie (wiertarka, szlifierka)",
                            "OsprzÄ™t - pÄ™kniÄ™te tarcze, zuĹĽyte wiertĹ‚a, Ĺşle zamocowane bity",
                            "HaĹ‚as w hali"
                        ],
                        "correctAnswer": 1
                    }
                ]
            },
            {
                "id": "content-8",
                "type": "content",
                "icon": "đźŚ§ď¸Ź",
                "subtitle": "MODUĹ 7/9",
                "title": "WARUNKI PRACY I TWOJA POZYCJA",
                "sections": [
                    {
                        "heading": "SprawdĹş miejsce",
                        "items": [
                            "czy nie ma wody / wilgoci",
                            "czy dobrze widzisz (Ĺ›wiatĹ‚o)",
                            "czy masz stabilne podĹ‚oĹĽe",
                            "czy nic nie leĹĽy pod nogami"
                        ]
                    },
                    {
                        "heading": "SprawdĹş siebie",
                        "items": [
                            "stoisz stabilnie",
                            "masz kontrolÄ™ nad narzÄ™dziem",
                            "nie pracujesz â€žna wyciÄ…gniÄ™tej rÄ™ce\""
                        ]
                    }
                ],
                "remember": {
                    "icon": "đź’ˇ",
                    "text": "ZĹ‚a pozycja = brak kontroli = wypadek."
                }
            },
            {
                "id": "content-9",
                "type": "content",
                "icon": "đźš§",
                "subtitle": "MODUĹ 8/9",
                "title": "ZABEZPIECZ STREFÄ PRACY",
                "sections": [
                    {
                        "heading": "Co to znaczy w praktyce",
                        "items": [
                            "nikt nie stoi w linii ciÄ™cia / odrzutu",
                            "narzÄ™dzia nie leĹĽÄ… na ziemi",
                            "kable sÄ… zabezpieczone",
                            "osoby postronne sÄ… poza strefÄ…"
                        ]
                    },
                    {
                        "heading": "Typowe bĹ‚Ä™dy",
                        "type": "warning",
                        "items": [
                            "âťŚ ktoĹ› stoi â€žtylko popatrzeÄ‡\"",
                            "âťŚ narzÄ™dzia pod nogami",
                            "âťŚ brak porzÄ…dku"
                        ]
                    }
                ],
                "remember": {
                    "icon": "đź’ˇ",
                    "text": "JeĹ›li ktoĹ› moĹĽe wejĹ›Ä‡ w twojÄ… strefÄ™ â€“ to teĹĽ twoja odpowiedzialnoĹ›Ä‡."
                }
            },
            {
                "id": "content-10",
                "type": "content",
                "icon": "đź§ ",
                "subtitle": "MODUĹ 9/9",
                "title": "ODPOWIEDZIALNOĹšÄ†",
                "sections": [
                    {
                        "heading": "Co to znaczy naprawdÄ™",
                        "type": "important",
                        "items": [
                            "Ty odpowiadasz za siebie",
                            "JeĹ›li ktoĹ› pracuje z tobÄ… â€“ odpowiadasz teĹĽ za niego",
                            "BezpieczeĹ„stwo to decyzje, nie gadanie"
                        ]
                    }
                ],
                "remember": {
                    "icon": "đź’ˇ",
                    "text": "Nie ma â€žna chwilÄ™\". Jest tylko â€žbezpiecznie\" albo â€žniebezpiecznie\"."
                }
            },
            {
                "id": "data-2",
                "type": "data",
                "icon": "đź“Š",
                "title": "LICZBY NIE KĹAMIÄ„",
                "subtitle": "Dlaczego przygotowanie do pracy ma znaczenie",
                "stats": [
                    {
                        "value": "67 000",
                        "label": "osĂłb poszkodowanych w wypadkach przy pracy w Polsce (2024)"
                    },
                    {
                        "value": "50%",
                        "label": "spadek wypadkĂłw w firmach ze szkoleniami BHP vs bez szkoleĹ„"
                    },
                    {
                        "value": "60%",
                        "label": "mniej urazĂłw przy prawidĹ‚owym uĹĽywaniu PPE (branĹĽe wysokiego ryzyka)"
                    }
                ],
                "callout": {
                    "type": "success",
                    "text": "ChoÄ‡ PPE wyglÄ…da jak drobna rzecz, to rĂłĹĽnica miÄ™dzy urazem a bezpiecznym dniem pracy."
                }
            },
            {
                "id": "quiz-final",
                "type": "quiz",
                "title": "đźŽŻ Test KoĹ„cowy - Project Zero",
                "subtitle": "10 pytaĹ„ sprawdzajÄ…cych TwojÄ… wiedzÄ™ z caĹ‚ej lekcji",
                "questions": [
                    {
                        "question": "Jakie 4 pytania zadajesz sobie przed robotÄ…?",
                        "options": [
                            "Gdzie, kiedy, z kim, ile",
                            "Co robiÄ™, z czego, co moĹĽe skrzywdziÄ‡, kto obok",
                            "Czy mam czas, czy mam narzÄ™dzie, czy wiem jak, czy ktoĹ› patrzy"
                        ],
                        "correctAnswer": 1,
                        "explanation": "To podstawa oceny ryzyka - 4 proste pytania, ktĂłre zajmujÄ… 30 sekund, ale mogÄ… uratowaÄ‡ zdrowie."
                    },
                    {
                        "question": "Kiedy PPE jest wĹ‚aĹ›ciwie dobrane?",
                        "options": [
                            "Gdy masz wszystko: okulary, rÄ™kawice, kask, buty",
                            "Gdy jest dopasowane do konkretnego zagroĹĽenia (pyĹ‚ â†’ maska, haĹ‚as â†’ nauszniki)",
                            "Gdy jest najnowszy model z certyfikatem"
                        ],
                        "correctAnswer": 1,
                        "explanation": "PPE dobierasz do roboty i zagroĹĽenia, nie na zasadzie \"wszystko na siebie\"."
                    },
                    {
                        "question": "Co robisz, gdy narzÄ™dzie siÄ™ grzeje i dĹ‚awi?",
                        "options": [
                            "Dociskam mocniej",
                            "Zmieniam narzÄ™dzie na mocniejsze lub sprawdzam osprzÄ™t",
                            "RobiÄ™ szybciej, ĹĽeby skoĹ„czyÄ‡"
                        ],
                        "correctAnswer": 1,
                        "explanation": "Grzanie i dĹ‚awienie to sygnaĹ‚, ĹĽe narzÄ™dzie nie pasuje do zadania."
                    },
                    {
                        "question": "Dlaczego osprzÄ™t jest groĹşniejszy niĹĽ samo narzÄ™dzie?",
                        "options": [
                            "Bo jest taĹ„szy",
                            "Bo pÄ™kniÄ™ta tarcza czy zuĹĽyty bit powodujÄ… wiÄ™kszoĹ›Ä‡ wypadkĂłw",
                            "Bo trudniej go wymieniÄ‡"
                        ],
                        "correctAnswer": 1,
                        "explanation": "Statystyki pokazujÄ…: najwiÄ™cej wypadkĂłw to pÄ™kniÄ™te tarcze, zuĹĽyte wiertĹ‚a i Ĺşle zamocowane bity."
                    },
                    {
                        "question": "Co to znaczy \"zabezpieczyÄ‡ strefÄ™ pracy\"?",
                        "options": [
                            "PostawiÄ‡ barierki dookoĹ‚a",
                            "UpewniÄ‡ siÄ™, ĹĽe nikt nie stoi w linii odrzutu, kable sÄ… bezpieczne, narzÄ™dzia nie leĹĽÄ… pod nogami",
                            "ZamknÄ…Ä‡ drzwi do pomieszczenia"
                        ],
                        "correctAnswer": 1,
                        "explanation": "Chodzi o praktyczne dziaĹ‚ania: kontrola strefy odrzutu, porzÄ…dek, bezpieczne kable."
                    },
                    {
                        "question": "Jak czÄ™sto sprawdzasz stan PPE?",
                        "options": [
                            "Raz w miesiÄ…cu",
                            "Przed kaĹĽdÄ… robotÄ…",
                            "Gdy coĹ› siÄ™ zepsuje"
                        ],
                        "correctAnswer": 1,
                        "explanation": "ZuĹĽyta ochrona nie chroni - sprawdzasz PRZED kaĹĽdÄ… robotÄ…."
                    },
                    {
                        "question": "Co robisz, gdy widzisz uszkodzonÄ… osĹ‚onÄ™ w narzÄ™dziu?",
                        "options": [
                            "PracujÄ™ ostroĹĽnie",
                            "Nie uĹĽywam narzÄ™dzia, naprawiam lub wymieniam osĹ‚onÄ™",
                            "ZgĹ‚aszam po zakoĹ„czeniu roboty"
                        ],
                        "correctAnswer": 1,
                        "explanation": "Uszkodzona osĹ‚ona = nie uĹĽywasz. Nie ma \"ostroĹĽnie\" z wirujÄ…cymi czÄ™Ĺ›ciami."
                    },
                    {
                        "question": "Dlaczego \"na chwilÄ™\" to najniebezpieczniejsze podejĹ›cie?",
                        "options": [
                            "Bo wtedy pomijamy ocenÄ™ ryzyka i PPE",
                            "Bo szef moĹĽe zobaczyÄ‡",
                            "Bo robota trwa dĹ‚uĹĽej"
                        ],
                        "correctAnswer": 0,
                        "explanation": "WiÄ™kszoĹ›Ä‡ wypadkĂłw dzieje siÄ™ przy robotach \"na chwilÄ™\", bo wtedy pomijamy podstawowe zasady."
                    },
                    {
                        "question": "Kto odpowiada za bezpieczeĹ„stwo na Twojej budowie/warsztacie?",
                        "options": [
                            "Szef / kierownik",
                            "SĹ‚uĹĽba BHP",
                            "Ty - za siebie i osoby w Twojej strefie"
                        ],
                        "correctAnswer": 2,
                        "explanation": "KaĹĽdy odpowiada za siebie i za osoby w swojej strefie pracy. To nie jest tylko zadanie BHP."
                    },
                    {
                        "question": "Co to znaczy Project Zero?",
                        "options": [
                            "Zero wypadkĂłw, zero kompromisĂłw - eliminowanie zagroĹĽeĹ„ zanim doprowadzÄ… do urazu",
                            "Zero kosztĂłw, zero strat",
                            "Zero narzÄ™dzi elektrycznych"
                        ],
                        "correctAnswer": 0,
                        "explanation": "Project Zero to globalna inicjatywa Milwaukee: zero wypadkĂłw przez edukacjÄ™, lepsze narzÄ™dzia i kulturÄ™ bezpieczeĹ„stwa."
                    }
                ]
            },
            {
                "id": "ending-1",
                "type": "ending",
                "icon": "âś…",
                "title": "GRATULACJE!",
                "subtitle": "UkoĹ„czyĹ‚eĹ› lekcjÄ™ Project Zero: Przygotowanie do Pracy",
                "checklist": [
                    {
                        "icon": "âś…",
                        "text": "Wiesz, jak zatrzymaÄ‡ siÄ™ przed robotÄ… i oceniÄ‡ ryzyko w 30 sekund"
                    },
                    {
                        "icon": "âś…",
                        "text": "Potrafisz dobraÄ‡ wĹ‚aĹ›ciwe PPE do zadania i sprawdziÄ‡ jego stan"
                    },
                    {
                        "icon": "âś…",
                        "text": "Rozumiesz, dlaczego osprzÄ™t wymaga szczegĂłlnej uwagi"
                    },
                    {
                        "icon": "âś…",
                        "text": "Znasz zasady zabezpieczania strefy pracy"
                    },
                    {
                        "icon": "âś…",
                        "text": "Rozumiesz, ĹĽe \"na chwilÄ™\" to najniebezpieczniejsze podejĹ›cie"
                    },
                    {
                        "icon": "âś…",
                        "text": "Znasz statystyki i realne przypadki z terenu"
                    }
                ],
                "tagline": "ZERO ACCIDENTS. ZERO COMPROMISES.",
                "next_steps": {
                    "text": "NastÄ™pna lekcja: **Bezpieczna Praca z NarzÄ™dziami Elektrycznymi**",
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
    RAISE NOTICE 'âś… Project Zero FULL lesson updated!';
    RAISE NOTICE 'đź“š Total cards: 20 (9 modules + quizzes + stories + data)';
    RAISE NOTICE 'âŹ±ď¸Ź Duration: 45 minutes';
    RAISE NOTICE 'âšˇ XP Reward: 200';
END $$;


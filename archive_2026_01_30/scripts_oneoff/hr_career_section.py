# HR Career Section for FMCG Game
# This will be integrated into the main game file

hr_career_section_code = '''
        # =============================
        # HR TAB: ŚCIEŻKA KARIERY
        # =============================
        with hr_tab_career:
            st.markdown("### 🎯 Ścieżka Kariery w FMCG")
            st.markdown("Twoja droga od Junior Sales Representative do Commercial Director")
            
            # Current position info
            current_level = game_state.get("career_level", 1)
            
            # Career levels definition
            career_levels = [
                {
                    "id": 1,
                    "name": "Junior Sales Representative",
                    "duration": "1-6 miesięcy",
                    "description": "Obsługa małych sklepów, podstawowa sprzedaż",
                    "requirements": "Podstawowe szkolenie produktowe",
                    "unlocks": ["Podstawowe wizyty", "Merchandising", "Reputacja klientów"]
                },
                {
                    "id": 2,
                    "name": "Sales Representative", 
                    "duration": "6 miesięcy - 2 lata",
                    "description": "Pełna odpowiedzialność za trasę, merchandising",
                    "requirements": "50 wizyt miesięcznie, podstawowe KPI",
                    "unlocks": ["Trudniejsi klienci", "Większy budżet", "Bonusy wynikowe"]
                },
                {
                    "id": 3,
                    "name": "Senior Sales Representative",
                    "duration": "2-3 lata", 
                    "description": "Obsługa trudniejszych klientów, mentoring juniorów",
                    "requirements": "100k PLN obrotów, certyfikat sprzedaży",
                    "unlocks": ["Mentoring", "Specjalne projekty", "Rozwój produktów"]
                },
                {
                    "id": 4,
                    "name": "Key Account Manager",
                    "duration": "3-5 lat",
                    "description": "Obsługa średnich/dużych sieci (Żabka, Carrefour)",
                    "requirements": "300k PLN obrotów, zespół 2-3 osób", 
                    "unlocks": ["Rekrutacja", "Negocjacje cenowe", "Planowanie kategorii"]
                },
                {
                    "id": 5,
                    "name": "Area Sales Manager",
                    "duration": "5-7 lat",
                    "description": "Zarządzanie obszarem (np. Śląsk), zespół sales repów",
                    "requirements": "Zespół 8-12 osób, budżet 1M PLN",
                    "unlocks": ["Zarządzanie zespołem", "Budżety regionalne", "Strategia obszaru"]
                },
                {
                    "id": 6,
                    "name": "Regional Sales Manager", 
                    "duration": "7-10 lat",
                    "description": "Zarządzanie regionem (np. Polska Południowa)",
                    "requirements": "3-4 obszary, zespół 30+ osób",
                    "unlocks": ["Strategia regionalna", "Cross-functional team", "P&L"]
                },
                {
                    "id": 7,
                    "name": "Trade Marketing Manager",
                    "duration": "8-11 lat", 
                    "description": "Strategie promocyjne, kategorie produktów",
                    "requirements": "Budżet marketingowy 2M PLN",
                    "unlocks": ["Kampanie 360°", "Category management", "Brand strategy"]
                },
                {
                    "id": 8,
                    "name": "Sales Director",
                    "duration": "10-15 lat",
                    "description": "Odpowiedzialność za całą sprzedaż w Polsce", 
                    "requirements": "P&L całego kanału, zespół 100+ osób",
                    "unlocks": ["Strategia sprzedaży", "Budżet krajowy", "Board meetings"]
                },
                {
                    "id": 9,
                    "name": "Commercial Director",
                    "duration": "15+ lat",
                    "description": "Strategia komercyjna, pricing, nowe rynki",
                    "requirements": "Doświadczenie międzynarodowe",
                    "unlocks": ["Ekspansja zagraniczna", "M&A", "Innovation pipeline"]
                }
            ]
            
            # Display career path
            for level in career_levels:
                is_current = level["id"] == current_level
                is_unlocked = level["id"] <= current_level
                is_next = level["id"] == current_level + 1
                
                # Card styling based on status
                if is_current:
                    card_color = "#22c55e"  # Green - current
                    status_text = "🎯 AKTUALNY POZIOM"
                    opacity = "1.0"
                elif is_next:
                    card_color = "#3b82f6"  # Blue - next target
                    status_text = "🎯 NASTĘPNY CEL"
                    opacity = "0.9"
                elif is_unlocked:
                    card_color = "#6b7280"  # Gray - completed
                    status_text = "✅ UKOŃCZONY"
                    opacity = "0.7"
                else:
                    card_color = "#9ca3af"  # Light gray - locked
                    status_text = "🔒 ZABLOKOWANY"
                    opacity = "0.5"
                
                with st.container():
                    st.markdown(f"""
                    <div style="border-left: 4px solid {card_color}; 
                                padding: 20px; 
                                margin: 15px 0; 
                                background: rgba(55, 65, 81, {opacity}); 
                                border-radius: 8px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <h4 style="margin: 0; color: {card_color};">{level['name']}</h4>
                            <span style="background: {card_color}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem;">
                                {status_text}
                            </span>
                        </div>
                        <p style="margin: 8px 0; color: #d1d5db;"><strong>Czas:</strong> {level['duration']}</p>
                        <p style="margin: 8px 0; color: #e5e7eb;">{level['description']}</p>
                        <p style="margin: 8px 0; color: #fbbf24;"><strong>Wymagania:</strong> {level['requirements']}</p>
                        <div style="margin-top: 12px;">
                            <strong style="color: #a78bfa;">Odblokowuje:</strong>
                            <ul style="margin: 5px 0 0 20px; color: #c4b5fd;">
                                {"".join([f"<li>{unlock}</li>" for unlock in level['unlocks']])}
                            </ul>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Progress to next level
            if current_level < len(career_levels):
                st.markdown("---")
                st.markdown("### 📊 Postęp do Następnego Poziomu")
                
                # Mock progress data - w przyszłości to będzie prawdziwe
                progress_data = {
                    "visits_completed": game_state.get("total_visits", 0),
                    "visits_required": 50,
                    "sales_current": game_state.get("monthly_sales", 0), 
                    "sales_required": 25000,
                    "reputation_avg": 3.2,  # Mock data
                    "reputation_required": 4.0
                }
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    visits_progress = min(100, (progress_data["visits_completed"] / progress_data["visits_required"]) * 100)
                    st.metric(
                        "Wizyty",
                        f"{progress_data['visits_completed']}/{progress_data['visits_required']}",
                        f"{visits_progress:.1f}%"
                    )
                    st.progress(visits_progress / 100)
                
                with col2:
                    sales_progress = min(100, (progress_data["sales_current"] / progress_data["sales_required"]) * 100)
                    st.metric(
                        "Sprzedaż miesięczna", 
                        f"{progress_data['sales_current']:.0f}/{progress_data['sales_required']} PLN",
                        f"{sales_progress:.1f}%"
                    )
                    st.progress(sales_progress / 100)
                
                with col3:
                    reputation_progress = min(100, (progress_data["reputation_avg"] / progress_data["reputation_required"]) * 100)
                    st.metric(
                        "Średnia reputacja",
                        f"{progress_data['reputation_avg']:.1f}/{progress_data['reputation_required']:.1f}",
                        f"{reputation_progress:.1f}%"
                    )
                    st.progress(reputation_progress / 100)
'''

print("HR Career section code created!")
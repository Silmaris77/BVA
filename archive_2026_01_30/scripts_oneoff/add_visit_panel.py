"""
Add visit execution panel to sales_tab_visit
Insert after the trial period/energy checks
"""

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find where to insert - before "# SUB-TAB: PRZYGOTOWANIE"
insert_idx = None
for i, line in enumerate(lines):
    if "# SUB-TAB: PRZYGOTOWANIE" in line and i > 4700:
        insert_idx = i
        break

if insert_idx is None:
    print("ERROR: Could not find insertion point")
    exit(1)

print(f"Will insert visit panel code at line {insert_idx + 1}")
print(f"Current line: {repr(lines[insert_idx][:60])}")

# Code to insert
visit_panel_code = '''
                # ============================================
                # VISIT EXECUTION PANEL
                # ============================================
                
                st.markdown("### 📋 Wybierz klienta do wizyty")
                
                # Get clients for visit
                available_clients = {
                    k: v for k, v in clients.items()
                    if v.get('status') != 'lost'
                }
                
                if not available_clients:
                    st.warning("Brak dostępnych klientów do odwiedzenia.")
                else:
                    # Client selection
                    client_names = {
                        client_id: f"{client.get('name', client_id)} ({client.get('type', 'Sklep')})"
                        for client_id, client in available_clients.items()
                    }
                    
                    selected_client_id = st.selectbox(
                        "Wybierz klienta:",
                        options=list(client_names.keys()),
                        format_func=lambda x: client_names[x],
                        key="visit_client_select"
                    )
                    
                    if selected_client_id:
                        selected_client = available_clients[selected_client_id]
                        
                        # Show client info
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Typ", selected_client.get('type', 'N/A'))
                        with col2:
                            rep = selected_client.get('reputation', 50)
                            st.metric("Reputacja", f"{rep}/100")
                        with col3:
                            dist = selected_client.get('distance_from_base', 0)
                            st.metric("Dystans", f"{dist:.1f} km")
                        
                        # Visit button
                        if st.button("🚗 Rozpocznij wizytę", type="primary", key="start_visit_btn"):
                            # Redirect to sales_tab_map where full visit UI is
                            st.info("💡 **Wskazówka**: Pełny panel wizyt z konwersacją AI znajduje się w zakładce **'🗺️ Klienci & Trasa'** → sekcja **'Planowanie trasy'** → wybierz klienta → **'Rozpocznij wizytę'**")
                            st.markdown("---")
                            st.markdown("**Przejdź do zakładki** `🗺️ Klienci & Trasa` i:")
                            st.markdown("1. Przewiń w dół do sekcji **'Planowanie trasy'**")
                            st.markdown("2. Wybierz klienta z listy")  
                            st.markdown("3. Kliknij **'Rozpocznij wizytę'**")
                
'''

# Insert the code
lines.insert(insert_idx, visit_panel_code)

print(f"Inserted visit panel code")

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("✅ Added visit execution panel to sales_tab_visit")

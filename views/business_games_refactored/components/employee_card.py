"""
Komponenty kart pracowników dla Business Games
Zawiera karty zatrudnionych i dostępnych pracowników
"""

import streamlit as st
from data.business_data import EMPLOYEE_TYPES
from utils.business_game import fire_employee, can_hire_employee, hire_employee
from data.users_new import save_single_user as save_user_data


def render_employee_card(employee, username, user_data, bg_data, industry_id="consulting"):
    """Renderuje kartę zatrudnionego pracownika - kompaktowa"""
    
    emp_data = EMPLOYEE_TYPES[employee["type"]]
    
    # Kompaktowa karta
    with st.container():
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 15px; border-radius: 10px; margin-bottom: 10px; color: white;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 18px; font-weight: bold;">{emp_data['ikona']} {emp_data['nazwa']}</div>
                    <div style="font-size: 12px; opacity: 0.9; margin-top: 4px;">{emp_data['bonus']}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 14px; font-weight: bold;">{emp_data['koszt_dzienny']} 💰/dzień</div>
                    <div style="font-size: 11px; opacity: 0.8;">od {employee['hired_date']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Przycisk zwolnienia
        if st.button("🗑️ Zwolnij", key=f"fire_{employee['id']}", type="secondary", use_container_width=True):
            updated_user_data, success, message = fire_employee(user_data, employee['id'], industry_id)
            if success:
                user_data.update(updated_user_data)
                save_user_data(username, user_data)
                st.success(message)
                st.rerun()
            else:
                st.error(message)


def render_hire_card(emp_type, emp_data, username, user_data, bg_data, industry_id="consulting"):
    """Renderuje kartę dostępnego pracownika - kompaktowa"""
    
    can_hire, reason = can_hire_employee(user_data, emp_type, industry_id)
    
    with st.container():
        # Kompaktowa karta z gradientem (szary)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #e0e0e0 0%, #bdbdbd 100%); 
                    padding: 15px; border-radius: 10px; margin-bottom: 10px; color: #424242;">
            <div style="font-size: 18px; font-weight: bold; margin-bottom: 8px;">
                {emp_data['ikona']} {emp_data['nazwa']}
            </div>
            <div style="font-size: 12px; opacity: 0.8; margin-bottom: 8px;">
                {emp_data['bonus']}
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 13px;">
                <div>💰 Zatrudnienie: <strong>{emp_data['koszt_zatrudnienia']}</strong></div>
                <div>📅 Dzienny: <strong>{emp_data['koszt_dzienny']}</strong></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Przycisk zatrudnienia
        if not can_hire:
            st.button("🔒 Niedostępny", key=f"hire_{emp_type}_locked", disabled=True, 
                     help=reason, use_container_width=True)
        else:
            if st.button("✅ Zatrudnij", key=f"hire_{emp_type}", type="primary", use_container_width=True):
                updated_user_data, success, message = hire_employee(user_data, emp_type, industry_id)
                if success:
                    user_data.update(updated_user_data)
                    save_user_data(username, user_data)
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        st.markdown("---")

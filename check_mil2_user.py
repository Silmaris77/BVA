#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sprawdzenie użytkownika mil2
"""

from database.models import User
from database.connection import session_scope

with session_scope() as session:
    user = session.query(User).filter_by(username='mil2').first()
    
    if user:
        print("=== UŻYTKOWNIK mil2 ===")
        print(f"Username: {user.username}")
        print(f"Company: {user.company}")
        print(f"Permissions: {user.permissions}")
        print(f"Created by: {user.account_created_by}")
    else:
        print("❌ Użytkownik mil2 nie istnieje!")

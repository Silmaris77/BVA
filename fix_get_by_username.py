"""
Skrypt do zamiany user_repo.get_by_username() na session.query(User).filter_by()
"""

import re
from pathlib import Path

files_to_fix = [
    "views/admin.py",
    "views/business_games.py",
    "views/inspirations.py",
    "utils/components.py"
]

def fix_file(filepath):
    """Zamienia get_by_username na query().filter_by()"""
    path = Path(filepath)
    
    if not path.exists():
        print(f"⚠️  Plik nie istnieje: {filepath}")
        return
    
    content = path.read_text(encoding='utf-8')
    original = content
    
    # Pattern: user_repo.get_by_username(username_var)
    # Replace with: session.query(User).filter_by(username=username_var).first()
    pattern = r'(\w+_repo)\.get_by_username\((\w+)\)'
    replacement = r'session.query(User).filter_by(username=\2).first()'
    
    content = re.sub(pattern, replacement, content)
    
    if content != original:
        # Dodaj import User na początku funkcji z session_scope
        # Znajdź pierwsze wystąpienie "with session_scope() as session:" i dodaj import przed nim
        import_line = "                from database.models import User\n"
        
        # Szukamy kontekstu z session_scope
        lines = content.split('\n')
        new_lines = []
        import_added = {}  # Track gdzie dodaliśmy import (per funkcja)
        
        for i, line in enumerate(lines):
            # Jeśli linia zawiera "with session_scope() as session:" i nie dodaliśmy jeszcze importu
            if 'with session_scope() as session:' in line:
                # Znajdź wcięcie
                indent = len(line) - len(line.lstrip())
                # Sprawdź czy import już nie istnieje w okolicy
                check_range = lines[max(0, i-5):i+5]
                has_import = any('from database.models import User' in l for l in check_range)
                
                if not has_import:
                    # Dodaj import z odpowiednim wcięciem przed session_scope
                    new_lines.append(' ' * indent + 'from database.models import User')
            
            new_lines.append(line)
        
        content = '\n'.join(new_lines)
        
        path.write_text(content, encoding='utf-8')
        print(f"✓ Poprawiono: {filepath}")
    else:
        print(f"  Bez zmian: {filepath}")

if __name__ == "__main__":
    print("Zamiana user_repo.get_by_username() na session.query()...")
    print("=" * 60)
    
    for file in files_to_fix:
        fix_file(file)
    
    print("=" * 60)
    print("Gotowe!")

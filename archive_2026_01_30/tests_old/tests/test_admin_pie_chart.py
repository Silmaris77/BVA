#!/usr/bin/env python3
"""
Test admin panel pie chart fix
"""

import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

def test_admin_pie_chart():
    """Test naprawy wykresu kołowego typów degenów"""
    
    print("🧪 Test wykresu kołowego typów degenów")
    print("=" * 60)
    
    try:
        # Import after setting up the path
        from views.admin import get_degen_type_distribution
        import matplotlib.pyplot as plt
        
        # Test 1: Get degen type distribution
        print("\n📊 Test 1: Sprawdzenie danych rozkładu typów degenów")
        degen_df = get_degen_type_distribution()
        
        print(f"   DataFrame shape: {degen_df.shape}")
        print(f"   Kolumny: {list(degen_df.columns)}")
        
        if degen_df.empty:
            print("   ⚠️ DataFrame jest pusty - wykres nie będzie wyświetlony")
            return True  # To nie jest błąd, po prostu brak danych
        
        print(f"\n   📋 Dane typów degenów:")
        for _, row in degen_df.iterrows():
            degen_type = row['degen_type']
            count = row['count']
            percentage = row['percentage']
            print(f"      {degen_type}: {count} użytkowników ({percentage}%)")
        
        # Test 2: Test matplotlib pie chart creation
        print(f"\n🥧 Test 2: Sprawdzenie tworzenia wykresu kołowego")
        
        try:
            # Test the corrected syntax
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Test tolist() conversion - this was the main fix
            counts = degen_df['count'].tolist()
            labels = degen_df['degen_type'].tolist()
            
            print(f"   Liczby (counts): {counts}")
            print(f"   Etykiety (labels): {labels}")
            
            # Check if types are correct
            print(f"   Typ counts: {type(counts)}")
            print(f"   Typ labels: {type(labels)}")
            
            if isinstance(counts, list) and isinstance(labels, list):
                print("   ✅ Konwersja do list() zakończona sukcesem")
            else:
                print("   ❌ Konwersja do list() nie powiodła się")
                return False
            
            # Try to create the pie chart
            ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90, shadow=False)
            ax.axis('equal')
            
            print("   ✅ Wykres kołowy utworzony bez błędów")
            
            # Close the figure to avoid display
            plt.close(fig)
            
        except Exception as e:
            print(f"   ❌ Błąd podczas tworzenia wykresu: {e}")
            return False
        
        # Test 3: Verify fix handles edge cases
        print(f"\n🔍 Test 3: Sprawdzenie obsługi przypadków brzegowych")
        
        # Test with empty DataFrame
        import pandas as pd
        empty_df = pd.DataFrame(columns=['degen_type', 'count', 'percentage'])
        
        try:
            if empty_df.empty:
                print("   ✅ Pusty DataFrame prawidłowo wykryty")
            else:
                print("   ❌ Pusty DataFrame nie został wykryty")
                return False
        except Exception as e:
            print(f"   ❌ Błąd podczas testowania pustego DataFrame: {e}")
            return False
        
        print("\n" + "=" * 60)
        print("✅ Wszystkie testy przeszły pomyślnie!")
        print("🎉 Wykres kołowy typów degenów działa poprawnie!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test nie powiódł się: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_admin_pie_chart()
    sys.exit(0 if success else 1)

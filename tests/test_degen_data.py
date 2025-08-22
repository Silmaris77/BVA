"""
Prosty test danych dla ulepszonego wykresu kołowego
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_degen_data():
    """Sprawdza dane typów degenów"""
    try:
        from views.admin import get_degen_type_distribution
        print("✅ Import funkcji get_degen_type_distribution")
        
        degen_df = get_degen_type_distribution()
        print(f"✅ Pobrano dane o typach degenów: {len(degen_df)} wierszy")
        
        if not degen_df.empty:
            print("\n📊 Rozkład typów degenów:")
            for _, row in degen_df.iterrows():
                print(f"   - {row['degen_type']}: {row['count']} ({row['percentage']}%)")
            
            # Sprawdź sumę procentów
            total_percentage = degen_df['percentage'].sum()
            print(f"\n✅ Suma procentów: {total_percentage}%")
            
            # Sprawdź, które typy będą miały widoczne etykiety (>=3%)
            visible_labels = degen_df[degen_df['percentage'] >= 3]
            print(f"✅ Typy z widocznymi etykietami (>=3%): {len(visible_labels)}")
            
            # Sprawdź, które segmenty będą wysunięte (<5%)
            small_segments = degen_df[degen_df['percentage'] < 5]
            print(f"✅ Małe segmenty do wysunięcia (<5%): {len(small_segments)}")
            
            return True
        else:
            print("❌ Brak danych o typach degenów")
            return False
            
    except Exception as e:
        print(f"❌ Błąd: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("TEST DANYCH WYKRESU KOŁOWEGO")
    print("=" * 50)
    
    success = test_degen_data()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Test danych przeszedł pomyślnie!")
    else:
        print("❌ Test danych nie przeszedł")
    print("=" * 50)

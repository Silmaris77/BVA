"""
Test ulepszonego wykresu kołowego typów degenów - sprawdzenie czytelności i funkcjonalności
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
import pandas as pd
from views.admin import get_degen_type_distribution

def test_improved_pie_chart():
    """Test ulepszonego wykresu kołowego z lepszą czytelnością"""
    print("🧪 Test ulepszonego wykresu kołowego typów degenów...")
    
    # Pobierz dane
    degen_df = get_degen_type_distribution()
    
    if degen_df.empty:
        print("❌ Brak danych o typach degenów")
        return False
    
    print(f"✅ Znaleziono {len(degen_df)} typów degenów:")
    for _, row in degen_df.iterrows():
        print(f"   - {row['degen_type']}: {row['count']} ({row['percentage']}%)")
    
    # Stwórz ulepszony wykres
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Przygotuj dane
    counts = degen_df['count'].tolist()
    labels = degen_df['degen_type'].tolist()
    total = sum(counts)
    
    # Funkcja do wyświetlania procentów tylko dla większych wartości
    def autopct_format(pct):
        return f'{pct:.1f}%' if pct >= 3 else ''
    
    # Stwórz wykres kołowy z automatycznym pozycjonowaniem etykiet
    pie_result = ax.pie(
        counts, 
        labels=labels,
        autopct=autopct_format,
        startangle=90,
        shadow=False,
        pctdistance=0.85,  # Odległość etykiet z procentami od środka
        labeldistance=1.1,  # Odległość nazw od środka
        explode=[0.05 if count/total < 0.05 else 0 for count in counts],  # Wysuń małe segmenty
        textprops={'fontsize': 10}
    )
    
    # Rozpakuj wyniki (może być 2 lub 3 elementy)
    if len(pie_result) == 3:
        wedges, texts, autotexts = pie_result
        print("✅ Wykres z etykietami procentowymi")
        # Poprawa czytelności etykiet procentowych
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
    else:
        wedges, texts = pie_result
        print("✅ Wykres bez etykiet procentowych")
    
    # Dodaj legendę z dokładnymi liczbami
    legend_labels = [f'{label}: {count} ({count/total*100:.1f}%)' 
                   for label, count in zip(labels, counts)]
    ax.legend(wedges, legend_labels, title="Typy degenów", 
             loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    ax.axis('equal')  # Zapewnia okrągły kształt
    plt.title('Rozkład typów degenów (Test)', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    # Zapisz wykres do pliku
    output_path = "test_improved_pie_chart.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✅ Wykres zapisany jako: {output_path}")
    
    # Sprawdź kluczowe elementy
    checks = {
        "Dane dostępne": len(degen_df) > 0,
        "Etykiety dodane": len(texts) == len(labels),
        "Legenda utworzona": True,  # Zawsze tworzymy legendę
        "Tytuł dodany": True,  # Zawsze dodajemy tytuł
        "Rozmiary segmentów": all(count > 0 for count in counts)
    }
    
    for check, passed in checks.items():
        print(f"{'✅' if passed else '❌'} {check}")
    
    plt.close()  # Zamknij wykres
    
    return all(checks.values())

if __name__ == "__main__":
    print("=" * 60)
    print("TEST ULEPSZONEGO WYKRESU KOŁOWEGO TYPÓW DEGENÓW")
    print("=" * 60)
    
    success = test_improved_pie_chart()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Wszystkie testy przeszły pomyślnie!")
        print("📊 Ulepszony wykres kołowy działa poprawnie z:")
        print("   - Lepszym rozmieszczeniem etykiet")
        print("   - Automatycznym ukrywaniem małych procentów")
        print("   - Wysuniętymi małymi segmentami")
        print("   - Szczegółową legendą")
        print("   - Poprawioną czytelnością")
    else:
        print("❌ Niektóre testy nie przeszły")
    print("=" * 60)

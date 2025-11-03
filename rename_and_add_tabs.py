"""
Simple solution: 
1. Rename current sales_tab_products (line 4728) to sales_tab_prep
2. Change its content to simple "w budowie"  
3. Add new sales_tab_products at the end with all product code
"""

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# 1. Find and rename sales_tab_products to sales_tab_prep
for i in range(4720, 4735):
    if "with sales_tab_products:" in lines[i]:
        lines[i] = "        with sales_tab_prep:\n"
        print(f"✅ Renamed at line {i+1}")
        break

# 2. Replace content of prep tab (lines 4729-4731) with simple message
lines[4728] = '            st.subheader("💼 Przygotowanie do Wizyt")\n'
lines[4729] = '            \n'
lines[4730] = '            st.info("""\n'
lines[4731] = '            🚧 **Sekcja w budowie**\n'
lines.insert(4732, '            \n')
lines.insert(4733, '            Tutaj będą dostępne narzędzia Trade-Marketing:\n')
lines.insert(4734, '            - 🎁 Planowanie promocji\n')
lines.insert(4735, '            - 📊 Analiza konkurencji\n')
lines.insert(4736, '            - 💰 Kalkulator marży\n')
lines.insert(4737, '            - 📋 Materiały POS\n')
lines.insert(4738, '            """)\n')
lines.insert(4739, '            \n')
lines.insert(4740, '            st.markdown("---")\n')
lines.insert(4741, '            st.markdown("💡 **Wskazówka**: Katalog produktów znajdziesz w zakładce **\'📦 Produkty\'**")\n')
lines.insert(4742, '        \n')

print("✅ Created simple prep tab")

with open(r"c:\Users\pksia\Dropbox\BVA\views\business_games_refactored\industries\fmcg_playable.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("✅ Now need to add sales_tab_products after prep")

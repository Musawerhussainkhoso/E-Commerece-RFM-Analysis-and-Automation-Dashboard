import sqlite3
from openpyxl import Workbook

print("=" * 80)
print("DAY 3: EXPORT RFM TO EXCEL")
print("=" * 80)

# Database se data nikalo
conn = sqlite3.connect('data/ecommerce.db')
cursor = conn.cursor()

print("\n1️⃣ Reading RFM data from database...")

cursor.execute('''
SELECT 
    c.customer_id,
    c.customer_name,
    c.city,
    MAX(o.order_date) as last_purchase,
    COUNT(o.order_id) as frequency,
    SUM(o.order_amount) as monetary
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.city
ORDER BY monetary DESC
''')

results = cursor.fetchall()

print(f"   ✓ {len(results)} customers ka data mil gaya")

# Excel workbook banao
print("\n2️⃣ Creating Excel workbook...")

wb = Workbook()
ws = wb.active
ws.title = "RFM Analysis"

# Headers likho
headers = ["Customer ID", "Name", "City", "Last Purchase", "Frequency", "Monetary"]
ws.append(headers)

# Data likho
print("\n3️⃣ Writing data to Excel...")

for row in results:
    ws.append(row)

print(f"   ✓ {len(results)} rows written")

# Formulas add karo
print("\n4️⃣ Adding formulas...")

last_row = len(results) + 2

# Total row
ws[f'A{last_row}'] = "TOTAL"
ws[f'E{last_row}'] = f'=SUM(E2:E{last_row-1})'
ws[f'F{last_row}'] = f'=SUM(F2:F{last_row-1})'

# Average row
ws[f'A{last_row+1}'] = "AVERAGE"
ws[f'E{last_row+1}'] = f'=AVERAGE(E2:E{last_row-1})'
ws[f'F{last_row+1}'] = f'=AVERAGE(F2:F{last_row-1})'

print("   ✓ Formulas added (SUM, AVERAGE)")

# Column width adjust
ws.column_dimensions['A'].width = 12
ws.column_dimensions['B'].width = 20
ws.column_dimensions['C'].width = 15
ws.column_dimensions['D'].width = 15
ws.column_dimensions['E'].width = 12
ws.column_dimensions['F'].width = 15

# Save karo
print("\n5️⃣ Saving Excel file...")

wb.save('output/rfm_analysis.xlsx')

print("   ✓ File saved: output/rfm_analysis.xlsx")

# Segment Summary Sheet
print("\n6️⃣ Creating segment summary...")

cursor.execute('''
SELECT 
    CASE 
        WHEN SUM(o.order_amount) > 150000 THEN 'VIP'
        WHEN SUM(o.order_amount) > 100000 THEN 'Loyal'
        WHEN SUM(o.order_amount) > 50000 THEN 'Regular'
        ELSE 'At Risk'
    END as segment,
    COUNT(c.customer_id) as count,
    SUM(o.order_amount) as total_revenue,
    AVG(o.order_amount) as avg_order
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY segment
ORDER BY total_revenue DESC
''')

segment_results = cursor.fetchall()

# Add segment sheet
ws2 = wb.create_sheet("Segment Summary")

ws2.append(["Segment", "Customer Count", "Total Revenue", "Average Order"])

for row in segment_results:
    ws2.append(row)

# Adjust column widths
ws2.column_dimensions['A'].width = 15
ws2.column_dimensions['B'].width = 18
ws2.column_dimensions['C'].width = 18
ws2.column_dimensions['D'].width = 18

# Save updated workbook
wb.save('output/rfm_analysis.xlsx')

print("   ✓ Segment summary added")

print("\n" + "=" * 80)
print("✅ DAY 3 COMPLETE!")
print("=" * 80)

print(f"\n📊 Output File: output/rfm_analysis.xlsx")
print(f"📋 Sheets: RFM Analysis, Segment Summary")

conn.close()
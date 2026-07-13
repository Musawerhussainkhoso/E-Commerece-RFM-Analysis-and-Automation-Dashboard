import sqlite3
from datetime import datetime

print("=" * 80)
print("DAY 2: RFM CALCULATION")
print("=" * 80)

conn = sqlite3.connect('data/ecommerce.db')
cursor = conn.cursor()

# Get RFM Data
print("\n Calculating RFM Data...\n")

cursor.execute('''
SELECT 
    c.customer_id,
    c.customer_name,
    MAX(o.order_date) as last_purchase,
    COUNT(o.order_id) as frequency,
    SUM(o.order_amount) as monetary
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY monetary DESC
''')

results = cursor.fetchall()

# Print Header
print(f"{'ID':<5} {'Name':<20} {'Last Buy':<12} {'Orders':<8} {'Total Spent':<12}")
print("-" * 80)

# Print Top 10 Customers
for i, row in enumerate(results[:10]):
    customer_id, name, last_buy, frequency, monetary = row
    print(f"{customer_id:<5} {name:<20} {last_buy:<12} {frequency:<8} {monetary:<12.0f}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"\nTotal Customers: {len(results)}")
print(f"Total Revenue: {sum(row[4] for row in results if row[4]):,.0f}")
print(f"Average Order Value: {sum(row[4] for row in results if row[4]) / len(results):,.0f}")

conn.close()

print("\n DAY 2 COMPLETE!")
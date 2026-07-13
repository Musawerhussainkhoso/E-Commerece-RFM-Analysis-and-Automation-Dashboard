import sqlite3
import csv

print("=" * 80)
print("DAY 4: EXPORT DATA FOR POWER BI")
print("=" * 80)

conn = sqlite3.connect('data/ecommerce.db')
cursor = conn.cursor()

# Export 1: RFM Data
print("\n1. Exporting RFM data...")

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

with open('output/rfm_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Customer ID', 'Name', 'City', 'Last Purchase', 'Frequency', 'Monetary'])
    writer.writerows(results)

print(f"   {len(results)} rows exported to rfm_data.csv")

# Export 2: Monthly Revenue
print("\n2. Exporting monthly revenue...")

cursor.execute('''
SELECT 
    strftime('%Y-%m', order_date) as month,
    COUNT(order_id) as total_orders,
    SUM(order_amount) as monthly_revenue
FROM orders
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month
''')

monthly_data = cursor.fetchall()

with open('output/monthly_revenue.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Month', 'Total Orders', 'Monthly Revenue'])
    writer.writerows(monthly_data)

print(f"   {len(monthly_data)} months exported to monthly_revenue.csv")

# Export 3: Customer Segment Data
print("\n3. Exporting customer segments...")

cursor.execute('''
SELECT 
    c.customer_id,
    c.customer_name,
    c.city,
    SUM(o.order_amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.city
ORDER BY total_spent DESC
''')

segment_data = cursor.fetchall()

# Add segment classification
segment_with_class = []
for row in segment_data:
    cust_id, name, city, total = row
    if total and total > 150000:
        segment = 'VIP'
    elif total and total > 100000:
        segment = 'Loyal'
    elif total and total > 50000:
        segment = 'Regular'
    else:
        segment = 'At Risk'
    segment_with_class.append((cust_id, name, city, total, segment))

with open('output/customer_segments.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Customer ID', 'Name', 'City', 'Total Spent', 'Segment'])
    writer.writerows(segment_with_class)

print(f"   {len(segment_with_class)} customers exported to customer_segments.csv")

# Export 4: City Analysis
print("\n4. Exporting city analysis...")

cursor.execute('''
SELECT 
    c.city,
    COUNT(c.customer_id) as customer_count,
    SUM(o.order_amount) as city_revenue,
    AVG(o.order_amount) as avg_order
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY city_revenue DESC
''')

city_data = cursor.fetchall()

with open('output/city_analysis.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['City', 'Customer Count', 'City Revenue', 'Average Order'])
    writer.writerows(city_data)

print(f"   {len(city_data)} cities exported to city_analysis.csv")

print("\n" + "=" * 80)
print("POWER BI EXPORT COMPLETE!")
print("=" * 80)

print("\nExported Files:")
print("   - output/rfm_data.csv")
print("   - output/monthly_revenue.csv")
print("   - output/customer_segments.csv")
print("   - output/city_analysis.csv")

conn.close()
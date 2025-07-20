import sqlite3
import numpy as np
import json

sql_file = "q-sql-correlation-github-pages.sql"  # <-- Path to the SQL file

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

with open(sql_file, "r") as f:
    sql_script = f.read()
cursor.executescript(sql_script)

query = """
SELECT Returns, Avg_Basket, Net_Sales
FROM retail_data
"""
rows = cursor.execute(query).fetchall()
conn.close()

returns = [row[0] for row in rows]
avg_basket = [row[1] for row in rows]
net_sales = [row[2] for row in rows]

def corr(x, y):
    return float(np.corrcoef(x, y)[0, 1])

pairs = {
    "Returns-Avg_Basket": corr(returns, avg_basket),
    "Returns-Net_Sales": corr(returns, net_sales),
    "Avg_Basket-Net_Sales": corr(avg_basket, net_sales),
}

strongest_pair = max(pairs.items(), key=lambda kv: abs(kv[1]))
result = {
    "pair": strongest_pair[0],
    "correlation": round(strongest_pair[1], 6)
}

print(json.dumps(result, indent=2))

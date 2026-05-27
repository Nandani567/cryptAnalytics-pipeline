import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor()

print("\n====== CRYPTO ANALYTICS ======\n")


cur.execute("SELECT COUNT(*) FROM trades")
totol_trades=cur.fetchone()[0]
print("Totol Trades: ", totol_trades)

cur.execute("SELECT MAX(price) FROM trades")
max_price=cur.fetchone()[0]
print("Maximum Price: " , max_price)

cur.execute("SELECT MIN(price) FROM trades")
min_price=cur.fetchone()[0]
print("Minimum Price: ",min_price)

cur.execute("SELECT AVG(price) FROM trades")
avg_price=cur.fetchone()[0]
print("Average Price: ",avg_price)

cur.execute("SELECT price FROM trades ORDER BY trade_id DESC LIMIT 1")
latest_price=cur.fetchone()[0]
print("Latest Price: ",latest_price)

cur.execute("SELECT MAX(quantity) FROM trades")
print(cur.fetchone()[0])

cur.execute("SELECT MAX(price) - MIN(price) FROM trades")
print(cur.fetchone()[0])

cur.execute("""
SELECT price
FROM trades
ORDER BY trade_id DESC
LIMIT 10
""")
print(cur.fetchall())

cur.execute("""
SELECT price
FROM trades
ORDER BY trade_id ASC
LIMIT 10
""")
print(cur.fetchall())

conn.close()
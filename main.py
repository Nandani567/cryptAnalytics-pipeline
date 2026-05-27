import websocket
import json
import psycopg2
import os
import time
from dotenv import load_dotenv

load_dotenv()

# ---------------- DB CONNECTION ----------------
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor()

# ---------------- TIME WINDOW ----------------
price_window = []   # (timestamp, price)

socket = "wss://stream.binance.com:9443/ws/btcusdt@trade"


# ---------------- MESSAGE HANDLER ----------------
def on_message(ws, message):

    global price_window

    data = json.loads(message)

    symbol = data["s"]
    price = float(data["p"])
    quantity = float(data["q"])
    trade_id = data["t"]
    event_time = data["E"]

    # ---------------- STORE IN DB ----------------
    cur.execute(
        """
        INSERT INTO trades (symbol, price, quantity, trade_id, event_time)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (symbol, price, quantity, trade_id, event_time)
    )

    conn.commit()

    # ---------------- TIME WINDOW (LAST 10 SEC) ----------------
    now = time.time()

    price_window.append((now, price))

    # keep only last 10 seconds
    price_window = [
        (t, p) for (t, p) in price_window
        if now - t <= 10
    ]

    # ---------------- SPIKE DETECTION ----------------
    if len(price_window) > 1:

        prices = [p for _, p in price_window]
        avg_price = sum(prices) / len(prices)

        threshold = avg_price * 0.002  # 0.2%

        if abs(price - avg_price) > threshold:
            print("SPIKE DETECTED (TIME WINDOW)")
            print("Price:", price)
            print("Avg:", avg_price)
            print("-----------------------------")

    # ---------------- DEBUG PRINT ----------------
    print(f"symbol: {symbol}")
    print(f"price: {price}")
    print(f"quantity: {quantity}")
    print(f"trade_id: {trade_id}")
    print(f"event_time: {event_time}")
    print("-----------------------------")


# ---------------- START WEBSOCKET ----------------
ws = websocket.WebSocketApp(socket, on_message=on_message)
ws.run_forever()
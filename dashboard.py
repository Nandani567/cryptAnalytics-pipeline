import streamlit as st
import pandas as pd
import psycopg2
import os
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

# ---------------- UI ----------------
st.title("Crypto Stream Dashboard (BTCUSDT)")

# ---------------- LOAD DATA ----------------
query = """
SELECT event_time, price, quantity
FROM trades
ORDER BY id DESC
LIMIT 200
"""

df = pd.read_sql(query, conn)

# sort for correct plotting
df = df.sort_values("event_time")

# ---------------- CHART ----------------
st.line_chart(df.set_index("event_time")["price"])

st.dataframe(df)
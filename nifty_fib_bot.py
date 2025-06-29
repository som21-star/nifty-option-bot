import os
import time
from datetime import datetime
from smartapi import SmartConnect
from telegram_alerts import send_telegram
from strike_selector import select_strike
from dotenv import load_dotenv

load_dotenv(".env")

API_KEY = os.getenv("API_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_PIN = os.getenv("CLIENT_PIN")

obj = SmartConnect(api_key=API_KEY)
session = obj.generateSession(CLIENT_ID, CLIENT_PIN)
access_token = session['data']['access_token']
obj.setAccessToken(access_token)

# Nifty token
NIFTY_TOKEN = "99926000"

# Define Fib Levels (percent-based example)
def fib_levels(base):
    return {
        '38.2': base * 1.382,
        '50': base * 1.5,
        '61.8': base * 1.618,
        '78.6': base * 1.786,
        '100': base * 2.0
    }

while True:
    try:
        nifty_price = obj.ltpData(exchange="NSE", tradingsymbol="NIFTY", symboltoken=NIFTY_TOKEN)['data']['ltp']
        strike, token = select_strike(obj, nifty_price)
        option_data = obj.ltpData(exchange="NFO", tradingsymbol=strike, symboltoken=token)
        premium = option_data['data']['ltp']
        fibs = fib_levels(premium)

        if fibs['50'] > premium > fibs['38.2']:
            message = f"\n✅ BUY SIGNAL\nStrike: {strike}\nPremium: {premium}\nNifty: {nifty_price}"
            send_telegram(message)
    except Exception as e:
        send_telegram(f"Error: {e}")
    time.sleep(900)  # every 15 min
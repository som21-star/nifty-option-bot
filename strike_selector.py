def select_strike(obj, spot_price, capital=15000, lot_size=50):
    atm_strike = int(round(spot_price / 50.0) * 50)
    otm_strike = atm_strike + 100
    tradingsymbol = f"NIFTY05JUL{otm_strike}CE"
    symboltoken = "123456"  # Replace with actual token
    return tradingsymbol, symboltoken
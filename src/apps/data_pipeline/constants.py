
VALID_SYMBOLS = [
    "NIFTY50",
    "RELIANCE",
    "TCS",
    "INFY",
    "HDFCBANK",
]

def is_valid_symbol(symbol: str) -> bool:
    return symbol in VALID_SYMBOLS
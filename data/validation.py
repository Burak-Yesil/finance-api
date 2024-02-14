import yfinance as yf

def is_valid_ticker(symbol):
    #Usage: checks to see if a ticker is valid
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1d")
    return not hist.empty


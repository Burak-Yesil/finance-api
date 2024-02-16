import aiohttp #Using this library instead of requests because the yahoo api was blocking the requests library
import asyncio
import json
from datetime import datetime, timedelta, timezone

async def fetch_stock_data(ticker, range='3mo'):
    #Usage: makes a get request to the yahoo finance api and returns the response
    if  not isinstance(ticker, str) or not isinstance(range, str):
        return {"connected_to_yahoo_finance": False, "response": None, "error": "parameters must be strings"}
    url = f"https://query1.finance.yahoo.com/v7/finance/chart/{ticker}?range={range}&interval=1d&indicators=quote&includeTimestamps=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                response_content = await response.read()
                return {"connected_to_yahoo_finance": True, "response": response_content}
            else:
                print("Error fetching data:", response.status)
                return {"connected_to_yahoo_finance": False, "response": None}


def calculate_day_over_day_changes(adjclose_values, date_times_est):
    #Usage: returns the day over day values for a given ticker 
    if  not isinstance(adjclose_values, list) or not isinstance(date_times_est, list):
        return {"day_over_day_changes": None, "error": "parameters most be lists"}
    day_over_day_changes = []
    pointer_current = 1
    pointer_previous = 0 #I used a two pointer approach - o(n) time complexity

    while pointer_current < len(adjclose_values):
        prev_value = adjclose_values[pointer_previous]
        current_value = adjclose_values[pointer_current]
        date = date_times_est[pointer_current]
        if prev_value != 0:
            change = 100 * (current_value / prev_value - 1)
        else: #Edge case - division by zero
            change = None
        day_over_day_changes.append({"date": date.strftime("%Y-%m-%d"), "move": change})

        pointer_previous += 1
        pointer_current += 1

    return {"day_over_day_changes": day_over_day_changes}


def top_five_day_over_day(ticker, range):
    #Usage: returns the top five day over day values and their dates given a ticker and range parameter.
    if  not isinstance(ticker, str) or not isinstance(range, str):
        return  {"json_parsed":False, "top_five_changes": None, "error": "parameters must be strings"}   
    valid_ranges = ["1mo", "3mo", "6mo", "1y", "2y"]
    if range not in valid_ranges:
        return {"json_parsed": False, "top_five_changes": None}    

    stock_data = asyncio.run(fetch_stock_data(ticker, range))
    if stock_data:
        stock_data = stock_data["response"]
        json_parsed = False
        response = json.loads(stock_data)
        result = response['chart']['result'][0]
        adjclose_values = result['indicators']['adjclose'][0]['adjclose']
        timestamps = result['timestamp']
        gmt_offset = result['meta']['gmtoffset']
        json_parsed=True
        est_offset = timedelta(seconds=-gmt_offset)
        date_times_est = [datetime.fromtimestamp(ts, tz=timezone(est_offset)) for ts in timestamps]

        day_over_day_changes = calculate_day_over_day_changes(adjclose_values, date_times_est)["day_over_day_changes"]

        top_five_changes = sorted(day_over_day_changes, key=lambda x: abs(x['move']), reverse=True)[:5]
        
        for i, obj in enumerate(top_five_changes):
            top_five_changes[i] = {"date": obj["date"], "move": str(round(obj["move"], 2))}

        return {"json_parsed":json_parsed, "top_five_changes": top_five_changes}    


import aiohttp #Using this library instead of requests because the yahoo api was blocking the requests library
import asyncio
import json
from datetime import datetime, timedelta, timezone

async def fetch_stock_data(ticker, range='3mo'):
    #Usage: makes a get request to the correct query1 yahoo finance api
    url = f"https://query1.finance.yahoo.com/v7/finance/chart/{ticker}?range={range}&interval=1d&indicators=quote&includeTimestamps=true"
    print(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                response_content = await response.read()
                return response_content
            else:
                print("Error fetching data:", response.status)
                return None

def calculate_day_over_day_changes(adjclose_values, date_times_est):
    day_over_day_changes = []
    pointer_current = 1
    pointer_previous = 0

    while pointer_current < len(adjclose_values):
        prev_value = adjclose_values[pointer_previous]
        current_value = adjclose_values[pointer_current]
        date = date_times_est[pointer_current]
        if prev_value != 0:
            change = 100 * (current_value / prev_value - 1)
        else: #Edge case - division by zero
            change = None
        day_over_day_changes.append({"date": date.strftime('%Y-%m-%d'), "move": change})

        pointer_previous += 1
        pointer_current += 1

    return day_over_day_changes


def top_five_day_over_day(ticker, range):
    stock_data = asyncio.run(fetch_stock_data(ticker, range))
    if stock_data:
        response = json.loads(stock_data)
        result = response['chart']['result'][0]
        adjclose_values = result['indicators']['adjclose'][0]['adjclose']
        timestamps = result['timestamp']
        gmt_offset = result['meta']['gmtoffset']
        est_offset = timedelta(seconds=-gmt_offset)
        date_times_est = [datetime.fromtimestamp(ts, tz=timezone(est_offset)) for ts in timestamps]


        # Calculate day-over-day percent change
        day_over_day_changes = calculate_day_over_day_changes(adjclose_values, date_times_est)

        top_five_changes = sorted(day_over_day_changes, key=lambda x: abs(x['move']), reverse=True)[:5]

        return top_five_changes    

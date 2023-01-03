import json
import os
import platform
import sys
from datetime import datetime, timedelta
from pprint import pprint
from time import time

import aiohttp
import asyncio


def get_dates(days_count):
    days = int(days_count)
    if days > 10:
        print("Sorry we can show Rates for 10 days or less.\n"
              "Input needle day's number in next time. Now show Rate for 10 days")
        days = 10
    today = datetime.today()
    return [(today - timedelta(days=_)).strftime('%d.%m.%Y') for _ in range(days)]


def get_currency_data(data, required_currency_list):
    currencies_data = [d for d in data['exchangeRate'] if d["currency"] in required_currency_list]
    all_currencies_info = {}
    for currency, currency_data in zip(required_currency_list, currencies_data):
        currency_exchange_info = {'sale': round(currency_data['saleRate'], 2),
                                  'purchase': round(currency_data['purchaseRate'], 2)}
        all_currencies_info.update({currency: currency_exchange_info})
    return {data['date']: all_currencies_info}


def write_json(data):
    if os.path.exists('exchangeRate.json'):
        json_data = json.load(open('exchangeRate.json'))
        json_data.append(data)
    else:
        json_data: list = [data]
    with open('exchangeRate.json', 'w') as file:
        json.dump(json_data, file, indent=2)


async def get_rate_for_date(session, url, required_currency_list):
    t0 = time()
    print(f'Get currency rate for {url[-10:]}...')
    try:
        async with session.get(url) as resp:
            print(f"Status for {url[-10:]}:", resp.status)
            if resp.status == 200:
                all_currencies = await resp.json()
                currency_data = get_currency_data(all_currencies, required_currency_list)
                write_json(currency_data)
                print(f'Get data time for {url[-10:]} = {time() - t0} sec\n')
                return currency_data
            else:
                print(f"Error status: {resp.status} for {url}")
    except aiohttp.ClientConnectorError as err:
        print(f'Connection error: {url}', str(err))


async def main(days_count):
    async with aiohttp.ClientSession() as session:
        urls = [f'https://api.privatbank.ua/p24api/exchange_rates?date={date}' for date in get_dates(days_count)]
        required_currency_list = ['USD', 'EUR']
        tasks = [asyncio.create_task(get_rate_for_date(session, url, required_currency_list)) for url in urls]
        responses = await asyncio.gather(*tasks)
        pprint(responses)


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    t = time()
    asyncio.run(main(sys.argv[1]))
    print(f'Main func execute time = {time() - t} sec')
#!/usr/bin/python3

from datetime import timedelta, datetime
import json
from time import sleep
import requests

import yfinance as yf

def get_prices(asset_list, start_date: str, end_date: str, timeframe: str):
    return yf.download(asset_list, start=start_date, end=end_date, interval=timeframe)

def format_data(raw_data):
    return raw_data.stack(level=1).rename_axis(['Date', 'Ticker']).reset_index()

def turn_json(raw_data) -> dict:
    return json.loads(raw_data.to_json(orient='table'))

def get_price_values(data):
    values_list = []
    for row in data['data']:
        values_list.append(
            {
                "read_date": row['Date'],
                "ticker": row['Ticker'].replace('.SA',''),
                "open_price": row['Open'],
                "high_price":row['High'],
                "low_price": row['Low'],
                "close_price": row['Adj Close'],
                "volume": row['Volume']
            }
        )
    return values_list

def get_tickers(base_url, endpoint, url_params):
    return requests.get(base_url + endpoint, params=url_params).json()

BRL_STOCKS_PARAMS = {"country_id": 1, "class_id": 1}
BRL_REITS_PARAMS = {"country_id": 1, "class_id": 2}
USD_STOCKS_PARAMS = {"country_id": 2, "class_id": 1}
USD_REITS_PARAMS = {"country_id": 2, "class_id": 3}
USD_ETFS_PARAMS = {"country_id": 2, "class_id": 4}

API_URL = 'http://nginx:9050'
TICKER_ENDPOINT = '/ticker_api'
INSERT_ENDPOINT = '/insert_quotes'
HEADERS = {'Content-Type': 'application/json', 'Accept':'application/json'}


if __name__ == '__main__':

    MARKET_TIME = datetime.strptime('10:20AM', '%I:%M%p').time()
    FORCE_RUN = False

    asset_class_list_tickers = [
        {'params': BRL_STOCKS_PARAMS, 'tickers': []},
        {'params': BRL_REITS_PARAMS, 'tickers': []},
        {'params': USD_STOCKS_PARAMS, 'tickers': []},
        {'params': USD_REITS_PARAMS, 'tickers': []},
        {'params': USD_ETFS_PARAMS,' tickers': []}
    ]

    for asset_class in asset_class_list_tickers:
        asset_class['tickers'] = get_tickers(API_URL, TICKER_ENDPOINT, asset_class['params'])
    
    while True:
        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date = str(datetime.now().date() + timedelta(days=1))
        timeframe = '5m'
        wait_seconds = 330

        if datetime.now().weekday() < 5 or FORCE_RUN:
            if datetime.now().time() >= MARKET_TIME or FORCE_RUN:
                print(f"READING DATA FROM: [ {start_date} ] ")
                print(f"TIMEFRAME: [ {timeframe} ] \n--------------------\n")
                
                for asset_class in asset_class_list_tickers:
                    try:
                        raw_data = get_prices(
                            asset_class['tickers'], start_date, end_date, timeframe
                        )

                        fmt_data = turn_json(format_data(raw_data))
                        stock_data = get_price_values(fmt_data)
                        requests.post(
                            API_URL + INSERT_ENDPOINT, 
                            json=stock_data,
                            headers=HEADERS
                            )
                    except:
                        Exception('Problem inserting')
                
                print(f'Waiting [ {wait_seconds} ] seconds for the next iteration')
                sleep(wait_seconds)
            else:
                print(f"It is [ {datetime.now().strftime('%a %H:%M')} ]! Markets are not open yet!")
                print("Next check in [ 1000 ] seconds!")
                sleep(1000)
        else:
            print(f"Today is [ {datetime.now().strftime('%A')} ]! Markets are not open yet!")
            print("Next check in [ 3600 ] seconds!")
            sleep(3600)

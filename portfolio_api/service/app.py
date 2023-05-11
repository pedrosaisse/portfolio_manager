
from fastapi import FastAPI
from repository.bd_utils import (
    get_data, insert_data, api_tickers, insert_quotes,
    wallet_balance, dividends_month
)
from domain.models import Assets, QuoteRate

app = FastAPI()

@app.get('/')
def index():
    return 'Hello Porra!!!'


@app.get('/get_assets/{country_id}')
def show_options(country_id):
    assets = get_data(country_id)
    return assets

@app.post('/add_asset')
def add_asset(asset: list[Assets]):
    return insert_data('assets', asset)


@app.get('/ticker_api')
def get_ticker_api(country_id: int, class_id: int, ignore: str = ''):
    ignore_list = ignore.split(',')
    return api_tickers(country_id, class_id, ignore_list)

@app.post('/insert_quotes')
def persist_quotes(quotes_data: list[QuoteRate]):
    insert_quotes(quotes_data)
    return 'OK'


@app.get('/current_position')
def wallet_position(class_id, country_id, wallet_id):
    return wallet_balance(wallet_id, country_id, class_id)

@app.get('/dividends')
def get_dividends_month(country_id: int, class_id: int):
    return dividends_month(country_id, class_id)

from datetime import datetime
from pydantic import BaseModel


class Assets(BaseModel):
    company: str
    ticker: str
    api_request_ticker: str
    position: float
    average_price: float
    country_id: int
    class_id: int
    wallet_id: int

class Country(BaseModel):
    country_id: int
    country_name: str
    iso_code: str

class Wallet(BaseModel):
    wallet_id: int
    wallet_name: str

class Dividends(BaseModel):
    ticker: str
    date_payment: datetime
    amount: float
    position: float
    currency: str
    country_id: int
    class_id: int
    payment_type_id: int

class QuoteRate(BaseModel):
    read_date: datetime
    ticker: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int

import uvicorn
from datetime import date, timedelta
from utils import ta_calculations as ta_calcs
from utils import functions as fnc
from utils import ohlc_values as ohlc
from utils import dollar_price as dllp
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Stock Market API",
    description="Get Stocks Prices, Technical Analysis Indicators and Dollar Prices",
    version="1.0.0"
)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['GET'],
    allow_headers=['Content-Type, Authorization'],
)


@app.get('/api/technical-analysis-between')
async def get_ta(ticker: str, indicator: str, start_date: str, end_date: str):
    print(f"indicator: {indicator}, ticker: {ticker}")

    indicator_values, str_dates = ta_calcs.get_indicator_values(ticker, indicator, start_date, end_date)

    ta = fnc.ta_json_format(ticker, indicator, indicator_values, str_dates)

    return jsonable_encoder(ta)


@app.get('/api/simple-technical-analysis')
async def get_simple_ta(ticker: str):
    simple_ta = ta_calcs.get_simple_ta(ticker)

    return jsonable_encoder(simple_ta)


@app.get('/api/price-between')
async def get_price_between(ticker: str, start_date: str, end_date: str):
    # date params format: YYYY/MM/DD

    data = ohlc.get_ohlc_between(ticker, start_date, end_date)

    return_json = {}
    return_json['ticker'] = ticker
    return_json['name'] = fnc.get_name(ticker)
    return_json['data'] = data

    return jsonable_encoder(return_json)


@app.get('/api/year-today-price')
async def get_year_today_prices(ticker: str):
    data = ohlc.get_ohlc_year_today(ticker)

    return_json = {}
    return_json['ticker'] = ticker
    return_json['name'] = fnc.get_name(ticker)
    return_json['data'] = data

    return jsonable_encoder(return_json)


@app.get('/api/ccl-cedear-dollar')
async def get_ccl_vs_cedear_dollar(ticker: str):
    data = dllp.calculate_difference(ticker)

    response = jsonable_encoder(data)
    return response


if __name__ == '__main__':
    uvicorn.run(app, port=5000)

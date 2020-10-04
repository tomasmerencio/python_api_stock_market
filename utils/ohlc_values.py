import json
import yahoo_fin.stock_info as yf
import pandas as pd
import utils.functions as fnc
from datetime import date, timedelta

DAYS = 365


def get_ohlc_values(ticker, start_date, end_date):
    # date params format: YYYY/MM/DD

    data = yf.get_data(ticker, start_date=start_date, index_as_date=False)

    # devolver inputs y lista de diccionarios con fecha, OHLC
    inputs = {
        'date': pd.Series(data['date']),
        'open': pd.Series(data['open'].round(2)),
        'high': pd.Series(data['high'].round(2)),
        'low': pd.Series(data['low'].round(2)),
        'close': pd.Series(data['close'].round(2)),
        'adjclose': pd.Series(data['adjclose'].round(2)),
        'volume': pd.Series(data['volume'].round(2))
    }

    dates_list = inputs['date'].tolist()

    str_dates = fnc.date_converter(dates_list)

    return inputs, str_dates


def apexcharts_ohlc_format(data_pandas):
    del data_pandas['ticker']

    data_json = data_pandas.to_json(orient='records')
    data_dict = json.loads(data_json)

    data_array = []

    for data in data_dict:
        data["date"] = int(data["date"])
        data["open"] = round(data["open"], 2)
        data["high"] = round(data["high"], 2)
        data["low"] = round(data["low"], 2)
        data["close"] = round(data["close"], 2)
        
        # item = [Timestamp, O, H, L, C]
        item = []
        ohlc_item = []
        
        item.append(data["date"])
        ohlc_item.append(data["open"])
        ohlc_item.append(data["high"])
        ohlc_item.append(data["low"])
        ohlc_item.append(data["close"])
        item.append(ohlc_item)

        data_array.append(item)
    
    return data_array


def get_ohlc_year_today(ticker):
    # date params format: YYYY/MM/DD
    start_date = date.today() - timedelta(days=DAYS)
    start_date = start_date.strftime("%Y/%m/%d")

    data = yf.get_data(ticker, start_date=start_date, index_as_date=False)
    
    data = apexcharts_ohlc_format(data)

    return data


def get_ohlc_between(ticker, start_date, end_date):
    # date params format: YYYY/MM/DD
    start_date = date.today() - timedelta(days=DAYS)
    start_date = start_date.strftime("%Y/%m/%d")

    data = yf.get_data(ticker, start_date=start_date, end_date= end_date, index_as_date=False)
    
    data = apexcharts_ohlc_format(data)

    return data
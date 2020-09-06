from datetime import date, timedelta
from utils import ta_calcs
from utils import functions as fnc
from flask import Flask, request, jsonify
from flask_cors import cross_origin


app = Flask(__name__)


@app.route('/api/ta', methods=['GET'])
@cross_origin(headers=["Access-Control-Allow-Origin", "*"])
def get_adx():
    ticker = request.args.get('ticker')
    indicator = request.args.get('indicator')
    print(f"indicator: {indicator}, ticker: {ticker}")

    # date params format: YYYY/MM/DD
    start_date = date.today() - timedelta(days=365)
    start_date = start_date.strftime("%Y/%m/%d")

    talib_inputs = ta_calcs.get_ohlc_values(ticker, start_date)

    indicator_values = ta_calcs.get_indicator_values(indicator, talib_inputs)

    talib_inputs = fnc.pd_series_to_list(talib_inputs)

    str_dates = fnc.date_converter(talib_inputs['date'])

    return_json = {}
    return_json['ticker'] = ticker
    return_json['name'] = fnc.get_name(ticker)
    return_json[f'{indicator}'] = indicator_values
    return_json['date'] = str_dates

    return jsonify(return_json)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)

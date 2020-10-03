from datetime import date, timedelta
from utils import ta_calculations as ta_calcs
from utils import functions as fnc
from utils import ohlc_values as ohlc
from utils import dollar_price as dllp
from flask import Flask, request, jsonify
from flask_cors import cross_origin


app = Flask(__name__)


@app.route('/api/ta', methods=['GET'])
def get_ta():
    ticker = request.args.get('ticker')
    indicator = request.args.get('indicator')
    print(f"indicator: {indicator}, ticker: {ticker}")

    indicator_values, str_dates = ta_calcs.get_indicator_values(ticker, indicator)

    ta = fnc.ta_json_format(ticker, indicator, indicator_values, str_dates)

    return jsonify(ta)


@app.route('/api/price-between', methods=['GET'])
def get_price_between():
    ticker = request.args.get('ticker')
    # date params format: YYYY/MM/DD
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    data = ohlc.get_ohlc_between(ticker, start_date, end_date)

    return_json = {}
    return_json['ticker'] = ticker
    return_json['name'] = fnc.get_name(ticker)
    return_json['data'] = data

    return jsonify(return_json)


@app.route('/api/year-today-price', methods=['GET'])
def get_year_today_prices():
    ticker = request.args.get('ticker')

    data = ohlc.get_ohlc_year_today(ticker)

    return_json = {}
    return_json['ticker'] = ticker
    return_json['name'] = fnc.get_name(ticker)
    return_json['data'] = data

    return jsonify(return_json)


@app.route('/ccl-cedear-dollar', methods=['GET'])
def get_ccl_vs_cedear_dollar():
    ticker = request.args.get('ticker')
    
    data = dllp.calculate_difference(ticker)

    response = jsonify(data)
    return response


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    header['Access-Control-Allow-Methods'] = 'GET'
    return response


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000)

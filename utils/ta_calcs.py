import yahoo_fin.stock_info as yf
import pandas_ta as ta
import pandas as pd


# cantidad de ultimos N items a retornar por lista
items_ret = 15


def get_ohlc_values(ticker, start_date):
    data = yf.get_data(ticker, start_date=start_date, index_as_date=False)

    # devolver inputs y lista de diccionarios con fecha, OHLC
    inputs = {
        'date': pd.Series(data['date']),
        'open': pd.Series(data['open']),
        'high': pd.Series(data['high']),
        'low': pd.Series(data['low']),
        'close': pd.Series(data['close']),
        'adjclose': pd.Series(data['adjclose']),
        'volume': pd.Series(data['volume'])
    }

    return inputs


def get_stoch_values(inputs):
    stoch_values = ta.stoch(inputs['high'], inputs['low'], inputs['close'])

    ret_dict = {}

    ret_dict['slowk'] = stoch_values['STOCHk_5'].values.tolist()[-items_ret:]
    ret_dict['slowd'] = stoch_values['STOCHd_3'].values.tolist()[-items_ret:]

    return ret_dict


def get_adx_values(inputs):
    adx_values = ta.adx(inputs['high'], inputs['low'], inputs['close'])

    ret_dict = {}

    ret_dict['adx'] = adx_values['ADX_14'].values.tolist()[-items_ret:]
    ret_dict['di_minus'] = adx_values['DMN_14'].values.tolist()[-items_ret:]
    ret_dict['di_plus'] = adx_values['DMP_14'].values.tolist()[-items_ret:]

    return ret_dict


def get_bbands_values(inputs):
    bbands_values = ta.bbands(inputs['close'])

    ret_dict = {}

    ret_dict['lower'] = bbands_values['BBL_5_2.0'].values.tolist()[-items_ret:]
    ret_dict['mid'] = bbands_values['BBM_5_2.0'].values.tolist()[-items_ret:]
    ret_dict['upper'] = bbands_values['BBU_5_2.0'].values.tolist()[-items_ret:]

    return ret_dict


def get_indicator_values(indicator, inputs):
    switcher = {
        'stoch': get_stoch_values(inputs),
        'adx': get_adx_values(inputs),
        'bbands': get_bbands_values(inputs)
    }

    return switcher.get(indicator, "Invalid Indicator")

import pandas_ta as ta
import utils.ohlc_values as ohlc


def get_stoch_values(inputs):
    stoch_values = ta.stoch(inputs['high'], inputs['low'], inputs['close'])

    ret_dict = {}

    ret_dict['slowk'] = stoch_values['STOCHk_5'].dropna().round(2).values.tolist()
    ret_dict['slowd'] = stoch_values['STOCHd_3'].dropna().round(2).values.tolist()

    return ret_dict


def get_adx_values(inputs):
    adx_values = ta.adx(inputs['high'], inputs['low'], inputs['close'])

    ret_dict = {}

    ret_dict['adx'] = adx_values['ADX_14'].dropna().round(2).values.tolist()
    ret_dict['di_minus'] = adx_values['DMN_14'].dropna().round(2).values.tolist()
    ret_dict['di_plus'] = adx_values['DMP_14'].dropna().round(2).values.tolist()

    return ret_dict


def get_bbands_values(inputs):
    bbands_values = ta.bbands(inputs['close'])

    ret_dict = {}

    ret_dict['lower'] = bbands_values['BBL_5_2.0'].dropna().round(2).values.tolist()
    ret_dict['mid'] = bbands_values['BBM_5_2.0'].dropna().round(2).values.tolist()
    ret_dict['upper'] = bbands_values['BBU_5_2.0'].dropna().round(2).values.tolist()

    return ret_dict


def get_indicator_values(ticker, indicator, start_date, end_date):

    inputs, str_dates = ohlc.get_ohlc_values(ticker, start_date, end_date)

    switcher = {
        'stoch': get_stoch_values(inputs),
        'adx': get_adx_values(inputs),
        'bbands': get_bbands_values(inputs)
    }

    indicator_values = switcher.get(indicator, "Invalid Indicator")

    return indicator_values, str_dates

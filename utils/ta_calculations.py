import pandas_ta as ta
import utils.ohlc_values as ohlc

# cantidad de ultimos N items a retornar por lista
ITEMS_RET = 365


def get_stoch_values(inputs):
    stoch_values = ta.stoch(inputs['high'], inputs['low'], inputs['close'])

    ret_dict = {}

    ret_dict['slowk'] = stoch_values['STOCHk_5'].values.tolist()[-ITEMS_RET:]
    ret_dict['slowd'] = stoch_values['STOCHd_3'].values.tolist()[-ITEMS_RET:]

    return ret_dict


def get_adx_values(inputs):
    adx_values = ta.adx(inputs['high'], inputs['low'], inputs['close'])

    ret_dict = {}

    ret_dict['adx'] = adx_values['ADX_14'].values.tolist()[-ITEMS_RET:]
    ret_dict['di_minus'] = adx_values['DMN_14'].values.tolist()[-ITEMS_RET:]
    ret_dict['di_plus'] = adx_values['DMP_14'].values.tolist()[-ITEMS_RET:]

    return ret_dict


def get_bbands_values(inputs):
    bbands_values = ta.bbands(inputs['close'])

    ret_dict = {}

    ret_dict['lower'] = bbands_values['BBL_5_2.0'].values.tolist()[-ITEMS_RET:]
    ret_dict['mid'] = bbands_values['BBM_5_2.0'].values.tolist()[-ITEMS_RET:]
    ret_dict['upper'] = bbands_values['BBU_5_2.0'].values.tolist()[-ITEMS_RET:]

    return ret_dict


def get_indicator_values(ticker, indicator):

    inputs, str_dates = ohlc.get_ohlc_values(ticker)

    switcher = {
        'stoch': get_stoch_values(inputs),
        'adx': get_adx_values(inputs),
        'bbands': get_bbands_values(inputs)
    }

    indicator_values = switcher.get(indicator, "Invalid Indicator")

    return indicator_values, str_dates[-ITEMS_RET:]

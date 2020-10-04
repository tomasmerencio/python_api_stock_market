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


def get_simple_ta(ticker):
    inputs, str_dates = ohlc.get_ohlc_days_ago(ticker, 30)

    stoch = get_stoch_values(inputs)
    adx = get_adx_values(inputs)
    bbands = get_bbands_values(inputs)

    stoch_simple_ta = get_stoch_simple_ta(stoch)
    adx_simple_ta = get_adx_simple_ta(adx)

    simple_ta = {}
    simple_ta['stoch'] = stoch_simple_ta
    simple_ta['adx'] = adx_simple_ta

    return simple_ta


def get_bbans_simple_ta(bbands):
    bbands['lower'] = bbands['lower'][-1:]
    bbands['mid'] = bbands['mid'][-1:]
    bbands['upper'] = bbands['upper'][-1:]

    return bbands


def get_adx_simple_ta(adx):
    print(adx)
    adx['adx'] = adx['adx'][-1:]
    adx['di_minus'] = adx['di_minus'][-1:]
    adx['di_plus'] = adx['di_plus'][-1:]

    adx['signal'] = 0

    if adx['adx'][0] > 25:
        if adx['di_minus'][0] > adx['di_plus'][0]:
            adx['signal'] = -1
        elif adx['di_plus'][0] > adx['di_minus'][0]:
            adx['signal'] = 1

    print(adx)

    return adx


def get_stoch_simple_ta(stoch):
    print(stoch)
    stoch['slowk'] = stoch['slowk'][-1:]
    stoch['slowd'] = stoch['slowd'][-1:]
    stoch['signal'] = 0

    if stoch['slowk'][0] > 80 and stoch['slowd'][0] > 80:
        stoch['signal'] = -1
    elif stoch['slowk'][0] < 20 and stoch['slowd'][0] < 20:
        stoch['signal'] = 1
    
    print(stoch)

    return stoch

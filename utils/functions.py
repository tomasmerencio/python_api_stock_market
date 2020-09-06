import cedears
from datetime import datetime

# cantidad de ultimos N items a retornar por lista
items_ret = 15


# obtener el nombre del cedear buscando por ticker
def get_name(ticker):
    for i in cedears.lista:
        if(i['ticker'] == ticker):
            return i['nombre']


# convertir fechas en formato epoch a YYYY/MM/DD
# devolver como lista
def date_converter(dates):
    str_dates = []
    for item in dates:
        item = datetime.utcfromtimestamp(item/1000000000).strftime('%Y/%m/%d')
        str_dates.append(item)

    return str_dates


# convertir serie pandas a lista
# devolver últimos items_ret
def pd_series_to_list(inputs):
    for key, value in inputs.items():
        inputs[key] = value.values.tolist()[-items_ret:]

    return inputs

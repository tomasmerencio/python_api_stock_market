import requests
import utils.functions as fnc
import yahoo_fin.stock_info as yf
from bs4 import BeautifulSoup

URL = "https://www.dolarhoy.com/cotizacion-dolar-ccl"

session = requests.Session()
session.get(URL)

def get_price(cotizacion):
    # page = requests.get(URL)
    page = session.get(URL)
    parsed_html = BeautifulSoup(page.content, "html.parser")
    cotizacion = parsed_html.find_all("div", class_="col-md-6 {}".format(cotizacion))
    cotizacion = cotizacion[0].findChild("h4").findChild("span").get_text()
    cotizacion = cotizacion.replace("$ ", "")
    cotizacion = cotizacion.replace(",", ".")
    fecha_actualizacion = parsed_html.find_all("span", class_="update")[0].get_text()
    return float(cotizacion), fecha_actualizacion


def calculate_difference(ticker):
    ratio = fnc.get_ratio(ticker)
    
    ccl_dollar, date_updated = get_price('venta')
    
    ba_price = round(yf.get_live_price(ticker + ".BA"), 2)
    us_price = round(yf.get_live_price(ticker), 2)

    data = {}
    data["ccl_dollar"] = ccl_dollar
    data["date_updated"] = date_updated
    data["ba_cedear_price"] = ba_price
    data["us_stock_price"] = us_price
    
    cedear_dollar = round((ba_price * ratio) / us_price, 2)
    
    difference = round((((cedear_dollar / ccl_dollar) * 100) - 100), 2)
    if cedear_dollar < ccl_dollar:
        difference = -abs(difference)

    data['ratio'] = ratio
    
    data["cedear_dollar"] = cedear_dollar
    
    data["difference"] = difference

    return data

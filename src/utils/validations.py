import pycountry

from src.utils.enums import PerPageSupport


def valid_currency(currency):
    try:
        pycountry.currencies.lookup(currency.upper())
    except LookupError:
        return False
    return True


def valid_countryCode(country):
    try:
        pycountry.countries.lookup(country.upper())
    except LookupError:
        return False
    return True

def vaild_per_page(per_page):
    try:
        PerPageSupport(per_page)
    except:
        return False
    return True
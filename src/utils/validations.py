import pycountry


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
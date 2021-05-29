import pycountry


def valid_currency(currency):
    try:
        pycountry.currencies.lookup(currency)
    except LookupError:
        return False
    return True

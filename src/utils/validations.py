import os
import re
from uuid import UUID

import pycountry

from config import settings
from src.utils.enums import PerPageSupport, AllowUserColumnOrderBy, AllowSortByDirection, RolesTypes


def valid_currency_code(currency):
    try:
        pycountry.currencies.lookup(currency.upper())
    except LookupError:
        return False
    return True


def valid_country_code(country):
    try:
        pycountry.countries.lookup(country.upper())
    except LookupError:
        return False
    return True


def check_email(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    # pass the regular expression
    # and the string in search() method
    if (re.search(regex, email)):
        return True

    else:
        return False


def vaild_per_page(per_page):
    try:
        PerPageSupport(per_page)
    except:
        return False
    return True


def check_string_not_empty(value, min_length=2, max_length=100):
    if not value:
        return False
    return min_length <= len(value) <= max_length


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """

    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def valid_user_list_params(filters, orders):
    filters['stores'] = list(filter(lambda x: is_valid_uuid(x), filters['stores']))  # will remove from query any in valid param
    filters['countries'] = list(filter(lambda x: valid_country_code(x), filters['countries']))  # will remove from query any in valid param
    filters['emails'] = list(filter(lambda x: check_email(x), filters['emails']))  # will remove from query any in valid param
    filters['names'] = list(filter(lambda x: check_string_not_empty(x), filters['names']))  # will remove from query any in valid param

    try:
        for order in orders:
            order['field'] = AllowUserColumnOrderBy(order['field'].lower())
            order['sort'] = AllowSortByDirection(order['sort'].lower())
    except:
        return False
    return {
        'filters': filters,
        'orders': orders
    }


def valid_user_list_by_permissions(userService, requester_uid, filters):
    user = userService.get_user(requester_uid, True)
    # check if requester user is platform user and have relevant roles allow to do query
    platform_roles = [
        RolesTypes.Owner.value,
        RolesTypes.Accounts.value,
        RolesTypes.Support.value,
        RolesTypes.Reports.value,
    ]
    if userService.user_has_any_role_matched(requester_uid, platform_roles):
        return filters
    # check if requester user is store user filter the stores filter to his register store_code and remove the rest
    store_roles = [
        RolesTypes.StoreOwner.value,
        RolesTypes.StoreAccount.value,
        RolesTypes.StoreReport.value,
        RolesTypes.StoreSupport.value,
    ]
    if userService.user_has_any_role_matched(requester_uid, store_roles) and user.store_code is not None:
        filters['stores'] = [user.store_code]  # we reset this flag allow only search by his own store not global search
        filters['platform'] = False
        filters['store_users'] = False
        return filters
    return False  # if this from customer or any type or role that not cover will auto reject

def media_type_valid(media_type):
    options = settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_TYPE_OPTIONS
    if media_type in options:
        return True
    return False
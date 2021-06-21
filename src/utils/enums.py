import os
from enum import Enum

class RolesTypes(Enum):
    Owner = 'owner'
    Reports = 'reports'
    Accounts = 'accounts'
    Support = 'support'
    StoreOwner = 'store_owner'
    StoreAccount = 'store_account'
    StoreCustomer = 'store_customer'
    StoreReport = 'store_reports'
    StoreSupport = 'store_support'


class AllowUserColumnOrderBy(Enum):
    CreateAt = "created_at"
    Fullname = "fullname"
    Email = "email"
    Country = "County"
    Store = "store_code"


class AllowSortByDirection(Enum):
    DESC = "desc"
    ASC = "asc"


class PerPageSupport(Enum):
    Per20 = 20
    Per30 = 30
    Per50 = 50
    Per75 = 75
    Per100 = 100
    Per200 = 200


class MediaAssetsType(Enum):
    Image = 1
    Video = 2
    Document = 3
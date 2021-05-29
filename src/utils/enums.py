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


class MediaAssetsType(Enum):
    Image = 1
    Video = 2
    Document = 3
    Unknown = 4

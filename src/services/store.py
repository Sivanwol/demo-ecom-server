from config.database import db
from sqlalchemy.sql import or_

from src.models.stores import Store
from src.schemas.store_schema import StoreSchema

storeSchema = StoreSchema()


class StoreService:

    def get_stores(self, return_model=False):
        stores = Store.query.all()
        if not return_model:
            return storeSchema.dumps(stores, many=True)
        return stores

    def get_store(self, owner_uid, store_code, return_model=False):
        store = Store.query.filter_by(owner_id=owner_uid, store_code=store_code).first()
        if store is None:
            return None
        if return_model:
            return storeSchema.dumps(store)
        return store

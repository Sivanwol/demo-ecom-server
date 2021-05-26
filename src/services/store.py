from config.api import cache
from config.database import db
import uuid

from src.exceptions.params_not_match_create_store import ParamsNotMatchCreateStore
from src.models.store_locations import StoreLocations
from src.models.stores import Store
from src.schemas.store_schema import StoreSchema, StoreLocationSchema
from src.utils.validations import valid_currency

storeSchema = StoreSchema()
storeLocationSchema = StoreLocationSchema()


class StoreService:
    @cache.memoize(50)
    def get_stores(self, return_model=False):
        stores = Store.query.all()
        if not return_model:
            return storeSchema.dumps(stores, many=True)
        return stores

    @cache.memoize(50)
    def get_store(self, owner_uid, store_code, return_model=False):
        store = Store.query.filter_by(owner_id=owner_uid, store_code=store_code).first()
        if store is None:
            return None
        if not return_model:
            return storeSchema.dumps(store)
        return store

    @cache.memoize(50)
    def get_locations(self, owner_uid, store_code):
        store = self.get_store(owner_uid, store_code, True)
        locations = StoreLocations.query.filter_by(store_id=store.id)
        return storeLocationSchema.dumps(locations, many=True)

    def update_locations(self, store_locations):
        bulk_locations = []
        for store_location in store_locations:
            bulk_locations.append(StoreLocations(store_location.store_id,
                                                 store_location.address,
                                                 store_location.city,
                                                 store_location.country_code,
                                                 store_location.lat,
                                                 store_location.lng,
                                                 store_location.is_close))
        db.session.bulk_save_objects(bulk_locations)
        db.session.commit()

    def remove_locations(self, store_id):
        StoreLocations.query.filter_by(store_id=store_id).delete()

    def create_store(self, store_object):
        if not valid_currency(store_object.default_currency_code):
            raise ParamsNotMatchCreateStore(store_object.owner_id, store_object.name, store_object.default_currency_code, store_object.logo_id,
                                            store_object.description)
        store_code = uuid.uuid4()
        store = Store(store_code, store_object.owner_id, store_object.name, store_object.default_currency_code, store_object.logo_id, store_object.description)
        db.session.add(store)
        db.session.commit()

    def clear_stores_cache(self):
        stores = self.get_stores()
        cache.delete_memoized('get_stores', True)
        cache.delete_memoized('get_stores', False)
        for store in stores:
            self.clear_store_cache(store.owner_id, store.store_code)

    def clear_store_cache(self, owner_uid, store_code):
        cache.delete_memoized('get_store', owner_uid, store_code, True)
        cache.delete_memoized('get_store', owner_uid, store_code, False)
        cache.delete_memoized('get_locations', owner_uid, store_code)

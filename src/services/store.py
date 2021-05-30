from sqlalchemy import desc

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
        stores = Store.query.order_by(desc(Store.created_at)).all()
        if not return_model:
            return storeSchema.dump(stores, many=True)

        return stores

    @cache.memoize(50)
    def get_store(self, owner_uid, store_code, return_model=False):
        store = Store.query.filter_by(owner_id=owner_uid, store_code=store_code).first()
        store_locations = StoreLocations.query.filter_by(store_id=store.id).all()
        if not return_model:
            return {
                'info': storeSchema.dump(store).data,
                'locations': storeLocationSchema.dump(store_locations, many=True).data
            }

        if store is None:
            return None
        return store

    @cache.memoize(50)
    def get_store_by_status_code(self, store_code, return_model=False):
        store = Store.query.filter_by(store_code=store_code).first()
        store_locations = StoreLocations.query.filter_by(store_id=store.id).all()
        if not return_model:
            return {
                'info': storeSchema.dump(store).data,
                'locations': storeLocationSchema.dump(store_locations, many=True).data
            }
        if store is None:
            return None
        return store

    @cache.memoize(50)
    def store_exists(self, owner_uid, store_code):
        store = Store.query.filter_by(owner_id=owner_uid, store_code=store_code).first()
        if store is None:
            return True
        return False

    @cache.memoize(50)
    def get_locations(self, store_id):
        store_locations = StoreLocations.query.filter_by(store_id=store_id).all()
        return store_locations

    def update_locations(self, owner_uid, store_code, store_locations):
        cache.delete_memoized(self.get_locations, owner_uid, store_code)
        self.remove_locations(owner_uid, store_code)
        bulk_locations = []
        store = self.get_store(owner_uid, store_code, True)
        for store_location in store_locations.locations:
            bulk_locations.append(StoreLocations(store.id,
                                                 store_location.address,
                                                 store_location.city,
                                                 store_location.country_code,
                                                 store_location.lat,
                                                 store_location.lng,
                                                 store_location.is_close))
        db.session.bulk_save_objects(bulk_locations, return_defaults=True)
        db.session.commit()
        return self.get_store(owner_uid, store_code)

    @cache.memoize(50)
    def get_hours(self, store_id):
        store_locations = StoreLocations.query.filter_by(store_id=store_id).all()
        return store_locations

    def update_hours(self, owner_uid, store_code, store_hours):
        cache.delete_memoized(self.get_hours, owner_uid, store_code)
        self.remove_locations(owner_uid, store_code)
        bulk_locations = []
        store = self.get_store(owner_uid, store_code, True)
        for store_hour in store_hours.hours:
            bulk_locations.append(StoreLocations(store.id,
                                                 store_location.address,
                                                 store_location.city,
                                                 store_location.country_code,
                                                 store_location.lat,
                                                 store_location.lng,
                                                 store_location.is_close))
        db.session.bulk_save_objects(bulk_locations, return_defaults=True)
        db.session.commit()
        return self.get_store(owner_uid, store_code)

    def update_store_info(self, owner_uid, store_code, store_object):
        if not valid_currency(store_object.currency_code):
            raise ParamsNotMatchCreateStore(owner_uid, store_object.name, store_object.currency_code, None, store_object.description)
        self.clear_stores_cache()
        store = self.get_store(owner_uid, store_code, True)
        store.name = store_object.name
        store.description = store_object.description
        store.default_currency_code = store_object.currency_code
        db.session.merge(store)
        db.session.commit()
        return self.get_store(owner_uid, store_code)

    def remove_locations(self, owner_uid, store_code):
        cache.delete_memoized(self.get_locations, owner_uid, store_code)
        store = self.get_store(owner_uid, store_code, True)
        StoreLocations.query.filter_by(store_id=store.id).delete()

    def create_store(self, owner_id, store_object):
        if not valid_currency(store_object['currency_code']):
            raise ParamsNotMatchCreateStore(owner_id, store_object['name'], store_object['currency_code'], None, store_object['description'])
        self.clear_stores_cache()
        store_code = "%s" % uuid.uuid4()
        store = Store(store_code, owner_id, store_object['name'], store_object['currency_code'], None, store_object['description'])
        db.session.add(store)
        db.session.commit()
        return self.get_store_by_status_code(store_code)

    def freeze_store(self, uid, store_code):
        self.clear_store_cache(uid, store_code)
        store = self.get_store(uid, store_code, True)
        store.is_maintenance = True
        db.session.merge(store)
        db.session.commit()

    def toggle_maintenance_store(self, owner_id, store_code):
        self.clear_store_cache(owner_id, store_code)
        store = self.get_store(owner_id, store_code, True)
        store.is_maintenance = not store.is_maintenance
        db.session.merge(store)
        db.session.commit()

    def clear_stores_cache(self):
        stores = self.get_stores(True)
        cache.delete_memoized(self.get_stores)
        for store in stores:
            self.clear_store_cache(store.owner_id, store.store_code)

    def clear_store_cache(self, owner_uid, store_code):
        cache.delete_memoized(self.get_store, owner_uid, store_code)
        cache.delete_memoized(self.get_locations, owner_uid, store_code)
        cache.delete_memoized(self.get_hours, owner_uid, store_code)

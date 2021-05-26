from config.api import cache, es
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
        if not return_model:
            stores = []
            res = es.search(index="stores", doc_type='metadata', body={"query": {"match_all": {}}})
            for doc in res['hits']['hits']:
                stores.append(doc['_source'])
            return storeSchema.dumps(stores, many=True)

        stores = Store.query.all()
        return stores

    @cache.memoize(50)
    def get_store(self, owner_uid, store_code, return_model=False):
        if not return_model:
            res = es.get(index="stores", doc_type='metadata', id=store_code)
            return storeSchema.dumps(res['_source'])

        store = Store.query.filter_by(owner_id=owner_uid, store_code=store_code).first()
        if store is None:
            return None
        return store

    @cache.memoize(50)
    def get_locations(self, owner_uid, store_code):
        store = self.get_store(owner_uid, store_code, True)
        search_param = {'query': {'match': {'store_id': store.id}}}
        locations = []
        res = es.search(index="stores", doc_type='metadata', body=search_param)
        for doc in res['hits']['hits']:
            locations.append(doc['_source'])
        return storeLocationSchema.dumps(locations, many=True)

    def update_locations(self, owner_uid, store_code, store_locations):
        cache.delete_memoized('get_locations', owner_uid, store_code)
        bulk_locations = []
        for store_location in store_locations:
            bulk_locations.append(StoreLocations(store_location.store_id,
                                                 store_location.address,
                                                 store_location.city,
                                                 store_location.country_code,
                                                 store_location.lat,
                                                 store_location.lng,
                                                 store_location.is_close))
        db.session.bulk_save_objects(bulk_locations, return_defaults=True)
        db.session.commit()
        for store_location in bulk_locations:
            es.index(index='stores', doc_type='locations', id=store_location.id, body=store_location)

    # Todo: add logic to update store meta data
    def update_store_metadata(self, store_data ):
        pass


    def remove_locations(self, owner_uid, store_code, store_id):
        cache.delete_memoized('get_locations', owner_uid, store_code)
        StoreLocations.query.filter_by(store_id=store_id).delete()
        search_param = {'query': {'match': {'store_id': store_id}}}
        res = es.search(index="stores", doc_type='metadata', body=search_param)
        for doc in res['hits']['hits']:
            location_id = doc['_id']
            es.delete(index='stores', doc_type='locations', id=location_id)

    def create_store(self, store_object):
        if not valid_currency(store_object.default_currency_code):
            raise ParamsNotMatchCreateStore(store_object.owner_id, store_object.name, store_object.default_currency_code, store_object.logo_id,
                                            store_object.description)
        store_code = uuid.uuid4()
        store = Store(store_code, store_object.owner_id, store_object.name, store_object.default_currency_code, store_object.logo_id, store_object.description)
        db.session.add(store)
        es.index(index='stores', doc_type='metadata', id=store_code, body=store)
        db.session.commit()

    def remove_store(self, store_code):
        Store.query.filter_by(store_code=store_code).delete()
        es.delete(index='stores', doc_type='metadata', id=store_code)

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

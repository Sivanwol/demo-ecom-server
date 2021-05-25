from config.database import db
from sqlalchemy.sql import or_

from src.models.store_locations import StoreLocations
from src.models.stores import Store
from src.schemas.store_location_schema import StoreLocationSchema
from src.schemas.store_schema import StoreSchema

storeSchema = StoreSchema()
storeLocationSchema = StoreLocationSchema()


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
        if not return_model:
            return storeSchema.dumps(store)
        return store

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

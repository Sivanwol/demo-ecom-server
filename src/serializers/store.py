from pydantic import BaseModel, constr


class StoreCreate(BaseModel):
    name = constr(max_length=100, min_length=3)
    description = constr(max_length=255)
    currency_code = constr(max_length=3, min_length=2)


class StoreUpdate(BaseModel):
    store_code = constr(max_length=100)
    name = constr(max_length=100, min_length=3)
    description = constr(max_length=255)
    currency_code = constr(max_length=3, min_length=2)

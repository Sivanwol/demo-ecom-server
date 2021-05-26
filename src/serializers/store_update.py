from pydantic import BaseModel, constr


class StoreUpdate(BaseModel):
    store_code = constr(max_length=100)
    name = constr(max_length=100)
    description = constr(max_length=255)
    currency_code = constr(max_length=3)

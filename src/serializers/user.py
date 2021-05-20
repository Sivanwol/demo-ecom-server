from pydantic import BaseModel, constr


class User(BaseModel):
    id: int
    uid: constr(max_length=100)  # https://pydantic-docs.helpmanual.io/usage/types/#constrained-types
    username: constr(max_length=20)
    password: constr(max_length=50)

    class Config:
        orm_mode = True

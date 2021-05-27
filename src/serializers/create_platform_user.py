from typing import List

from pydantic import BaseModel, constr


class CreatePlatformUser(BaseModel):
    role_names: List[constr(max_length=255)]

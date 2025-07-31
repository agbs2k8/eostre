import config as cfg
import pydantic
from dataclasses import dataclass


class UserInput(pydantic.BaseModel):
    username: str
    password: str

# NOTE - TO USE A LIST OF UuserInput values, would need to do the following:
# from typing import List

# @validate_request(List[Person])
# @app.post("/")
# async def index():
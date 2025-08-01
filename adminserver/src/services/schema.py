import config as cfg
import pydantic
import typing
from dataclasses import dataclass


class UserInput(pydantic.BaseModel):
    # NOTE - ... means required field. 
    username: str = pydantic.Field(..., description="The username")
    password: str = pydantic.Field(..., description="The user-provided password")
    email: str = pydantic.Field(None, description="The user's email address")

# NOTE - TO USE A LIST OF UuserInput values, would need to do the following:
# from typing import List

# @validate_request(List[Person])
# @app.post("/")
# async def index():

class RefreshTokenInput(pydantic.BaseModel):
    refresh_token: str

    class Config:
        # Can also use BaseModel.Config.extra = "allow"
        extra = "allow" 

class BaseRequest(pydantic.BaseModel):
    request_id: str = pydantic.Field(..., description="Unique ID for this request")
    client_version: str = pydantic.Field(..., description="Client version string")

    class Config:
        extra = "allow"  # Allow extra fields in all subclasses

class LoginRequest(BaseRequest):
    username: str = pydantic.Field(..., description="The username")
    password: str = pydantic.Field(..., description="The password")

class SignupRequest(BaseRequest):
    email: str
    password: str
    name: str


# QUERY STRING EXAMPLE
# from quart_schema import validate_querystring

# class QueryParams(BaseModel):
#     limit: int
#     offset: int

# @my_bp.route("/items", methods=["GET"])
# @validate_querystring(QueryParams)
# async def get_items(query: QueryParams):
#     return {"limit": query.limit, "offset": query.offset}

# URL PARAMETERS EXAMPLE
# Quart itself handles route parsing (/users/<int:user_id>), but you can manually validate it using Pydantic if needed:

# NOTE - quart-schema doesn't support header validation directly,

# Validate headers, body, and query-string togeher:
# @my_bp.route("/complex", methods=["POST"])
# @validate_request(MyBody)
# @validate_querystring(QueryParams)
# async def complex(data: MyBody, query: QueryParams):
#     headers = HeaderModel(
#         x_api_key=request.headers.get("X-API-Key"),
#         user_agent=request.headers.get("User-Agent")
#     )
#     ...
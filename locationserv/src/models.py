import datetime
from bson import ObjectId
from pydantic import (BaseModel, 
                      Field,
                      conlist, 
                      GetJsonSchemaHandler, 
                      model_validator, 
                      GetCoreSchemaHandler)
from pydantic_core import core_schema
from typing import Optional, List, Dict, Literal, Any
from src.helpers import drop_null_keys


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        from pydantic_core import core_schema

        def validate(value):
            if isinstance(value, ObjectId):
                return value
            if not ObjectId.is_valid(value):
                raise ValueError(f"Invalid ObjectId: {value}")
            return ObjectId(value)

        return core_schema.no_info_after_validator_function(
            validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    

class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(alias="_name")
    account_id: str
    created_by: str
    created_date: Optional[datetime.datetime] = Field(default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc))
    modified_date: Optional[datetime.datetime] = Field(default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc))
    modified_by: Optional[str] = None
    deleted: bool = False
    deleted_date: Optional[datetime.datetime] = None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }

    @classmethod
    def model_serializer(cls, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return obj

    def to_dict(self, use:str="return") -> dict:
        if use == "return":
            _dict = drop_null_keys(self.model_dump(by_alias=False))
            _dict["id"] = str(_dict["id"])
            return _dict
        else:
            # by_alias converts to _name and _id
            _dict = self.model_dump(by_alias=True)
            # ensure we're writing the _id as an ObjectId instance
            _dict["_id"] = ObjectId(str(_dict["_id"]))
            return _dict
    
    
    async def insert(self, db_client):
        # Happy path result:InsertOneResult('<id-value>', acknowledged=True)
        result = await db_client.locations.insert_one(self.to_dict(use="insert"))
        if result.acknowledged:
            return (True, self)
        else:
            raise (False, self)
    
    async def update(self, db_client):
        # Happy Path: "UpdateResult({'n': 1, 'electionId': ObjectId('7f...fe'), 'opTime': {'ts': Timestamp(17...25, 76), 't': 510},
        #                            'nModified': 1, 'ok': 1.0, '$clusterTime': {'clusterTime': Timestamp(1754...25, 76), 
        #                             'signature': {'hash': b'\\xb...\\x19', 'keyId': 75...84}}, 
        #                             'operationTime': Timestamp(1754940725, 76), 'updatedExisting': True}, acknowledged=True)"
        result = await db_client.locations.update_one(
                {"_id": ObjectId(str(self.id))},  # Force _id to be an ObjectId instance
                {"$set": self.to_dict(use="update")},
                upsert=True
            )
        if result.acknowledged:
            return (True, self)
        else:
            raise (False, self)


class AddressDistrict(BaseModel):
    name: Optional[str]
    shortName: Optional[str]

class CountryRegion(BaseModel):
    name: Optional[str]

class Address(BaseModel):
    countryRegion: Optional[CountryRegion]
    addressLine: Optional[str]
    adminDistricts: Optional[List[AddressDistrict]]
    formattedAddress: Optional[str]
    locality: Optional[str]
    postalCode: Optional[str]
    streetName: Optional[str]
    streetNumber: Optional[str]

class GeoPoint(BaseModel):
    type: Literal['Point']
    coordinates: conlist(float, min_length=2, max_length=3)  # Lon, Lat,  elev.

    @model_validator(mode="before")
    @classmethod
    def validate_coordinates(cls, values):
        lon, lat = values.get("coordinates")[:2]
        if not (-180 <= lon <= 180):
            raise ValueError(f"Longitude {lon} out of bounds (-180 to 180).")
        if not (-90 <= lat <= 90):
            raise ValueError(f"Latitude {lat} out of bounds (-90 to 90).")
        return values


class Location(MongoBaseModel):
    display_name: Optional[str] = None
    active: bool = True
    geo_point: GeoPoint
    address: Address

    @staticmethod
    def deserialize(doc: dict) -> Optional["Location"]:
        if doc is None:
            return None
        return Location(**doc)
    
    @staticmethod
    async def get(id, db_client):
        """Retrieve a location by a specific field and value"""
        location_raw = await db_client.locations.find_one({"_id": ObjectId(id)})
        return Location.deserialize(location_raw) if location_raw else None
    
    async def update_fields(self, db_client, **kwargs):
        mutable_fields = ["deleted", "deleted_date", "active", "display_name", "geo_point", "address", "modified_date", "modified_by"]
        for key, value in kwargs.items():
            if key in mutable_fields and getattr(self, key) != value:
                setattr(self, key, value)
        return await self.update(db_client)


class LocationListResponse(BaseModel):
    data: List[Location]
import fastapi
import datetime
from typing import Optional, List
from bson import ObjectId
from src.models import Location
from src.db import get_db
from src.token_manager import token_manager

router = fastapi.APIRouter()

@router.get("/liveness")
async def liveness():
    return {"message": "ok"}

@router.get("/readiness")
async def readiness():
    return {"message": "ok"}


@router.get("/locations")
async def list_locations_open(
    db = fastapi.Depends(get_db),
    ids: Optional[List[str]] = fastapi.Query(default=None, alias="id")#,
    #user: dict = fastapi.Depends(token_manager.require_permissions("account.read"))
):
    account_id = "1"#str(user["account_id"])
    filter_query = {"account_id":account_id} 
    if ids:
        object_ids = [ObjectId(id_) for id_ in ids]
        filter_query = filter_query | {"_id":{"$in": object_ids}}
    else:
        filter_query = filter_query | {"deleted": False, "active": True}  # Everything not deleted
    cursor = db["locations"].find(filter_query)
    docs = await cursor.to_list(length=None)
    locations = [Location.deserialize(doc).to_dict() for doc in docs]
    return {"data": locations}


@router.get("/location")
async def list_locations(
    db = fastapi.Depends(get_db),
    ids: Optional[List[str]] = fastapi.Query(default=None, alias="id"),
    user: dict = fastapi.Depends(token_manager.require_permissions("account.read"))
):
    account_id = str(user["account_id"])
    filter_query = {"account_id":account_id} 
    if ids:
        object_ids = [ObjectId(id_) for id_ in ids]
        filter_query = filter_query | {"_id":{"$in": object_ids}}
    else:
        filter_query = filter_query | {"deleted": False, "active": True}  # Everything not deleted
    cursor = db["locations"].find(filter_query)
    docs = await cursor.to_list(length=None)
    locations = [Location.deserialize(doc).to_dict() for doc in docs]
    return {"data": locations}


@router.post("/location")
async def add_location(
    location: Location,
    db = fastapi.Depends(get_db),
    user: dict = fastapi.Depends(token_manager.require_permissions("account.write"))
):
    
    # Ensure the created_by/modified_by both are set appropriately
    location.created_by = user["sub"]
    location.modified_by = user["sub"]
    # Double Check the account_id values(s)
    account_id = str(user["account_id"])
    if location.account_id != account_id:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="The account_id value of the object does not match the account_id of the user."
        )
    success, location = await location.insert(db)  # TODO -Add error handling on write of the object
    if success:
        return {"message": "OK", "inserted_data":location.to_dict()}
    else:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_500,
            detail="Unable to write to DB."
        )


@router.put("/location")
async def update_location(
    location: Location,
    db = fastapi.Depends(get_db),
    user: dict = fastapi.Depends(token_manager.require_permissions("account.write"))
):
    # Check ID
    if not location.id:
        raise fastapi.HTTPException(
            status_cod=fastapi.status.HTTP_400_BAD_REQUEST,
            detai="the id value for the location is required for updates."
        )
    # Get the Location object from the database
    db_location = await Location.get(location.id, db)
    if not db_location:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="The location was not found."
        )
    # Double Check the account_id values(s)
    account_id = str(user["account_id"])
    if location.account_id != account_id:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="The account_id value of the object does not match the account_id of the user."
        )
    # The fields from the API-provided location combined with modified_by/date
    updates = {"modified_date": datetime.datetime.now(tz=datetime.timezone.utc), 
               "modified_by":user["sub"]}
    updates = location.to_dict() | updates
    
    # Make the updates using the Location instance originally from the Database
    success, db_location = await db_location.update_fields(db, **updates)
    if success:
        return {"message": "OK", "inserted_data":db_location.to_dict()}
    else:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_500,
            detail="Unable to write to DB."
        )
    
@router.delete("/location")
async def delete_location(
    location: Location,
    db = fastapi.Depends(get_db),
    user: dict = fastapi.Depends(token_manager.require_permissions("account.write"))
):
    # Check ID
    if not location.id:
        raise fastapi.HTTPException(
            status_cod=fastapi.status.HTTP_400_BAD_REQUEST,
            detai="the id value for the location is required for updates."
        )
    # Get the Location object from the database
    db_location = await Location.get(location.id, db)
    if not db_location:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="The location was not found."
        )
    # Double Check the account_id values(s)
    account_id = str(user["account_id"])
    if location.account_id != account_id:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="The account_id value of the object does not match the account_id of the user."
        )
    # The fields from the API-provided location combined with modified_by/date
    updates = {"modified_date": datetime.datetime.now(tz=datetime.timezone.utc), 
               "modified_by":user["sub"],
               "deleted": True,
               "active": False,
               "deleted_date": datetime.datetime.now(tz=datetime.timezone.utc)}
    updates = location.to_dict() | updates
    
    # Make the updates using the Location instance originally from the Database
    success, db_location = await db_location.update_fields(db, **updates)
    if success:
        return {"message": "OK", "inserted_data":db_location.to_dict()}
    else:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_500,
            detail="Unable to write to DB."
        )
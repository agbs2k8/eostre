import pymongo 
from config import cfg

client: pymongo.AsyncMongoClient | None = None

def init_db():
    global client
    mongo_conn_string = f"mongodb+srv://{cfg.DATABASE_USER}:{cfg.DATABASE_PASSWORD}@{cfg.DATABASE_URL}/?retryWrites=true&w=majority&appName={cfg.APP_NAME}"
    client = pymongo.AsyncMongoClient(mongo_conn_string)
    return client

def get_db():
    if client is None:
        raise RuntimeError("MongoDB client has not been initialized.")
    return client[cfg.DATABASE_NAME]


async def ensure_indexes(db: pymongo.AsyncMongoClient):
    await db.locations.create_index(
        [("geo_point", pymongo.GEOSPHERE)],
        name="geo_point_2dsphere"
    )

    await db.locations.create_index(
        [("_name", pymongo.ASCENDING), ("account_id", pymongo.ASCENDING)],
        name="name_account_idx",
        unique=True
    )
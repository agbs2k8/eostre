from mongomock import MongoClient as SyncMongoClient
from unittest.mock import MagicMock
import types

class AsyncCursor:
    def __init__(self, sync_cursor):
        self._sync_cursor = sync_cursor

    async def to_list(self, length=None):
        # mongomock's cursor is already a list-like object
        return list(self._sync_cursor)[:length]

    def __aiter__(self):
        self._iter = iter(self._sync_cursor)
        return self

    async def __anext__(self):
        try:
            return next(self._iter)
        except StopIteration:
            raise StopAsyncIteration

class AsyncCollection:
    def __init__(self, sync_collection):
        self._sync_collection = sync_collection

    async def insert_one(self, doc):
        return self._sync_collection.insert_one(doc)

    async def update_one(self, *args, **kwargs):
        return self._sync_collection.update_one(*args, **kwargs)

    async def find_one(self, *args, **kwargs):
        return self._sync_collection.find_one(*args, **kwargs)

    def find(self, *args, **kwargs):
        return AsyncCursor(self._sync_collection.find(*args, **kwargs))

    async def create_index(self, *args, **kwargs):
        return self._sync_collection.create_index(*args, **kwargs)

class AsyncDatabase:
    def __init__(self, sync_db):
        self._sync_db = sync_db

    def __getitem__(self, name):
        return AsyncCollection(self._sync_db[name])

    @property
    def locations(self):
        return AsyncCollection(self._sync_db.locations)

class AsyncMongoMockClient:
    def __init__(self, *args, **kwargs):
        self._sync_client = SyncMongoClient()
    def __getitem__(self, name):
        return AsyncDatabase(self._sync_client[name])
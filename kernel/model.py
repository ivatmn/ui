import inspect
import os
import sys
from hashlib import md5

from peewee import *
from playhouse.pool import PooledPostgresqlExtDatabase

DB_CONFIG = {
    'database': 'postgres',
    'user': 'postgres',
    'password': '123456',
    'host': '127.0.0.1',
    'port': '5432',
    'max_connections': 32,
    'stale_timeout': 300,
    'register_hstore': False,
    'autocommit': True,
    'autorollback': True
    # 'async': True
}

db = PooledPostgresqlExtDatabase(**DB_CONFIG)


def create_all_tables():
    for cls in sys.modules[__name__].__dict__.values():
        if hasattr(cls, '_meta') and inspect.isclass(cls) and issubclass(cls, Model):
            if cls is not BaseModel:
                cls.create_table()

class BaseModel(Model):
    class Meta:
        database = db


class Office(BaseModel):
    code = TextField(unique=True)
    name = TextField()
    tags = TextField(null=True)
    comment = TextField(null=True)

    class Meta:
        db_table = 'k_offices'
        schema = 'kernel'
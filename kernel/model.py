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
    code = CharField(unique=True)
    name = CharField()

    class Meta:
        db_table = 'k_offices'
        schema = 'kernel'


class User(BaseModel):
    office = ForeignKeyField(Office)
    login = CharField(unique=True)
    passord = CharField(max_length=255)
    is_enable = BooleanField(default=True)
    

    class Meta:
        db_table = 'k_users'
        schema = 'kernel'
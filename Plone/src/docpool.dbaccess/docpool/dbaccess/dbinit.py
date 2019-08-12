from sqlalchemy.schema import ThreadLocalMetaData
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import scoped_session, sessionmaker, relation
from sqlalchemy import create_engine
import os
from elixir import *

db_string = os.environ.get('ELANDB', 'elan')
db_host = os.environ.get('ELANHOST', 'localhost')
db_complete = os.environ.get('ELANENGINE', None)
__metadata__ = metadata
if db_complete:
    __metadata__.bind = create_engine("%s" % (db_complete), echo=False)
else:
    __metadata__.bind = create_engine(
        "postgres://elan:elan@%s:5432/%s" % (db_host, db_string), echo=False
    )
__session__ = scoped_session(
    sessionmaker(
        bind=__metadata__.bind,
        autocommit=False,
        twophase=False,
        autoflush=True,
        extension=ZopeTransactionExtension(),
    )
)

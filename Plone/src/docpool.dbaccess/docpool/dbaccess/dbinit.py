from elixir import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

import os


db_string = os.environ.get('ELANDB', 'elan')
db_host = os.environ.get('ELANHOST', 'localhost')
db_complete = os.environ.get('ELANENGINE', None)
__metadata__ = metadata
if db_complete:
    __metadata__.bind = create_engine("%s" % (db_complete), echo=False)
else:
    __metadata__.bind = create_engine(
        "postgres://elan:elan@{}:5432/{}".format(db_host, db_string), echo=False
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

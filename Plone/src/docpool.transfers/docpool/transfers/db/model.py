# -*- coding: utf-8 -*-
__author__ = 'Condat AG'
__docformat__ = 'plaintext'

from datetime import datetime
from docpool.dbaccess.dbinit import __metadata__
from docpool.dbaccess.dbinit import __session__
from elixir import DateTime
from elixir import Entity
from elixir import Field
from elixir import setup_all
from elixir import String
from elixir import Unicode
from elixir import using_options

import logging


metadata = __metadata__
session = __session__


DEBUG = 0
__metadata__.bind.echo = False
if DEBUG:
    __metadata__.bind.echo = True
logger = logging.getLogger("docpool.transfers")


class Channel(Entity):
    """
    """

    using_options(tablename='channels')

    title = Field(Unicode(128))
    esd_from_uid = Field(String(50))
    esd_from_title = Field(Unicode(100))
    tf_uid = Field(String(50))
    esd_to_title = Field(Unicode(100))
    timestamp = Field(DateTime(), default=datetime.now)


setup_all(create_tables=True)

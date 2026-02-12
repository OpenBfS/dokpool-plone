from datetime import datetime
from docpool.elan.config import ELAN_APP
from OFS.interfaces import IObjectWillBeRemovedEvent
from plone import api
from plone.dexterity.content import Container
from plone.restapi.serializer.converters import json_compatible
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer

import json


class IELANArchive(model.Schema):
    """ """


@implementer(IELANArchive)
class ELANArchive(Container):
    """ """

    APP = ELAN_APP

    def myELANArchive(self):
        """ """
        return self

    def get_archived_event(self):
        """Get the DPEvent of this archive."""
        brains = api.content.find(
            context=self,
            portal_type="DPEvent",
        )
        if brains and len(brains) == 1:
            return brains[0].getObject()


@adapter(IELANArchive, IObjectWillBeRemovedEvent)
def delete_handler(obj, event):
    """
    Log info on deleted archives.
    """
    parent = obj.__parent__
    data = json.loads(parent.deleted_archives) if parent.deleted_archives else []
    plone_view = api.content.get_view("plone", obj)
    new = [plone_view.toLocalizedTime(datetime.now(), long_format=1), api.user.get_current().id, obj.title]
    data.append(new)
    parent.deleted_archives = json.dumps(json_compatible(data))

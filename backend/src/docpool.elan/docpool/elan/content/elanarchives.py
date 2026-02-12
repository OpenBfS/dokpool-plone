from docpool.elan.config import ELAN_APP
from plone.dexterity.content import Container
from plone.schema.jsonfield import JSONField
from plone.supermodel import model
from zope.interface import implementer


class IELANArchives(model.Schema):
    """ """

    deleted_archives = JSONField(
        title="Log of deleted Archives",
        required=False,
    )


@implementer(IELANArchives)
class ELANArchives(Container):
    """ """

    APP = ELAN_APP

from docpool.base.content.dpdocument import IAppSpecificWorkflow
from docpool.base.content.dpdocument import IDPDocument
from docpool.elan.config import ELAN_APP
from plone import api
from zope.component import adapter
from zope.interface import implementer
from zope.interface import named


@adapter(IDPDocument)
@implementer(IAppSpecificWorkflow)
@named(ELAN_APP)
class ELANSpecificWorkflow:
    def __init__(self, context):
        self.context = context

    def is_transition_allowed(self, transition):
        # disallow retracting a published ELAN document except for the server admin
        if not (transition == "retract" and api.content.get_state(self.context) == "published"):
            return True
        return "Manager" in api.user.get_roles()

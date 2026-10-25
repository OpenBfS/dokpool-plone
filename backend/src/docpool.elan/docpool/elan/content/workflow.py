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
        roles = api.user.get_roles(obj=self.context)
        if transition == "retract":
            # Retracting is only for published ELAN entries except for managers
            # See https://redmine-koala.bfs.de/issues/6342
            review_state = api.content.get_state(self.context)
            if review_state == "published":
                return "Manager" in roles
        if transition == "revoke":
            # Revoke is only for ELAN entries and only for certain roles
            # See https://redmine-koala.bfs.de/issues/6853
            return set(roles) & {"Manager", "Site Administrator", "Owner"}

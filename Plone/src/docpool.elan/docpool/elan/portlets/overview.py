from Acquisition import aq_chain
from Acquisition import aq_inner
from docpool.base.content.archiving import IArchiving
from docpool.elan import DocpoolMessageFactory as _
from docpool.elan.utils import getScenariosForCurrentUser
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer

import plone.api as api


# This interface defines the configurable options (if any) for the portlet.
# It will be used to generate add and edit forms. In this case, we don't
# have an edit form, since there are no editable options.


class IOverviewPortlet(IPortletDataProvider):
    pass


# The assignment is a persistent object used to store the configuration of
# a particular instantiation of the portlet.


@implementer(IOverviewPortlet)
class Assignment(base.Assignment):
    @property
    def title(self):
        return _("Overview")


# The renderer is like a view (in fact, like a content provider/viewlet). The
# item self.data will typically be the assignment (although it is possible
# that the assignment chooses to return a different object - see
# base.Assignment).


class Renderer(base.Renderer):

    # render() will be called to render the portlet

    render = ViewPageTemplateFile("overview.pt")

    @property
    def available(self):
        has_current_situation = hasattr(self.context, "myELANCurrentSituation")
        return has_current_situation and not self.isEditMode()

    def isEditMode(self):
        """ """
        path = self.request.get("PATH_INFO", "")
        if path.endswith("/edit") or path.endswith("/@@edit"):
            return True

    def specialObjects(self):
        """ """
        return [o for o in self._specialObjects() if o.id not in ("recent", "overview")]

    def _specialObjects(self):
        cs = self.context.myELANCurrentSituation()
        yield from cs.getFolderContents(
            {
                "portal_type": [
                    "Dashboard",
                ]
            }
        )

        # In archive we only return the archived journals
        if IArchiving(self.context).is_archive:
            for item in aq_chain(aq_inner(self.context)):
                if getattr(item, "portal_type", None) == "ELANArchive":
                    yield from api.content.find(context=item, portal_type="Journal")
                    return
            return

        # Get the active journals for this scenario and document pool
        scenarios = getScenariosForCurrentUser()
        dp = self.context.myDocumentPool()
        # User could select more than one scenario
        for scenario in scenarios:
            event_brain = api.content.find(
                portal_type="DPEvent",
                context=dp,
                id=scenario,
            )
            if event_brain:
                yield from api.content.find(
                    portal_type="Journal",
                    path=event_brain[0].getPath(),
                )


class AddForm(base.NullAddForm):

    # This method must be implemented to actually construct the object.

    def create(self):
        return Assignment()

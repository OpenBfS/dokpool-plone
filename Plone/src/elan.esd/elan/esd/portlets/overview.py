# -*- coding: utf-8 -*-
from Acquisition import aq_chain
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from docpool.event.utils import getScenariosForCurrentUser
from elan.esd import DocpoolMessageFactory as _
from plone import api
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope.interface import implementer

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
        return _(u"Overview")


# The renderer is like a view (in fact, like a content provider/viewlet). The
# item self.data will typically be the assignment (although it is possible
# that the assignment chooses to return a different object - see
# base.Assignment).


class Renderer(base.Renderer):

    # render() will be called to render the portlet

    render = ViewPageTemplateFile('overview.pt')

    @property
    def available(self):
        return self.context.isCurrentSituation() and not self.isEditMode()

    def isEditMode(self):
        """
        """
        path = self.request.get("PATH_INFO", "")
        if path.endswith("/edit") or path.endswith("/@@edit"):
            return True

    def specialObjects(self):
        """
        """
        return [o for o in self._specialObjects() if o.id not in ('recent', 'overview')]

    def _specialObjects(self):
        cs = self.context.myELANCurrentSituation()
        for obj in cs.getFolderContents(
            {
                'portal_type': [
                    'Dashboard',
                    'SituationOverview',
                ]
            }
        ):
            yield obj

        # In archive we only return the archived journals
        if self.context.isArchive():
            for item in aq_chain(aq_inner(self.context)):
                if getattr(item, "portal_type", None) == "ELANArchive":
                    for journal in api.content.find(context=item, portal_type="Journal"):
                        yield journal
                    return
            return

        # Get the active journals for this scenario and document pool
        scenarios = getScenariosForCurrentUser(self.context)
        dp = self.context.myDocumentPool()
        # User could select more than one scenario
        for scenario in scenarios:
            event_brains = api.content.find(
                portal_type='DPEvent',
                context=dp,
                UID=scenario,
            )
            # Since we reference scenarios by id, which may be shared, our best
            # guess is to use the first one found that is not archived.
            for brain in event_brains:
                if "archive" in brain.getPath().split("/"):
                    continue
                for brain in api.content.find(portal_type="Journal", path=brain.getPath()):
                    yield brain
                break


class AddForm(base.NullAddForm):

    # This method must be implemented to actually construct the object.

    def create(self):
        return Assignment()

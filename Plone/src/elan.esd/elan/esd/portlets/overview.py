# -*- coding: utf-8 -*-

from elan.esd import DocpoolMessageFactory as _
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements


# This interface defines the configurable options (if any) for the portlet.
# It will be used to generate add and edit forms. In this case, we don't
# have an edit form, since there are no editable options.


class IOverviewPortlet(IPortletDataProvider):
    pass


# The assignment is a persistent object used to store the configuration of
# a particular instantiation of the portlet.


class Assignment(base.Assignment):
    implements(IOverviewPortlet)

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
        cs = self.context.myELANCurrentSituation()
        fc = cs.getFolderContents(
            {
                'portal_type': [
                    'ELANDocCollection',
                    'Dashboard',
                    'SituationOverview',
                    'Journal',
                ]
            }
        )
        return [o for o in fc if o.id not in ('recent', 'overview')]


class AddForm(base.NullAddForm):

    # This method must be implemented to actually construct the object.

    def create(self):
        return Assignment()

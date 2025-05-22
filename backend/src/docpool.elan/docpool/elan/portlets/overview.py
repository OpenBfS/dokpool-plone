from Acquisition import aq_chain
from Acquisition import aq_inner
from docpool.base.content.archiving import IArchiving
from docpool.elan import DocpoolMessageFactory as _
from docpool.elan.utils import getScenariosForCurrentUser
from plone import api
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer


class IOverviewPortlet(IPortletDataProvider):
    pass


@implementer(IOverviewPortlet)
class Assignment(base.Assignment):
    @property
    def title(self):
        return _("Overview")


class Renderer(base.Renderer):
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
        if getattr(self.context, "myDocumentPool", None) is None:
            # Not within a docpool
            return

        cs = self.context.myELANCurrentSituation()
        yield from api.content.find(
            context=cs,
            portal_type="Dashboard",
            sort_on="getObjPositionInParent",
        )

        # In archive we only return the archived journals
        if IArchiving(self.context).is_archive:
            for item in aq_chain(aq_inner(self.context)):
                if getattr(item, "portal_type", None) == "ELANArchive":
                    yield from api.content.find(
                        context=item,
                        portal_type="Journal",
                        sort_on="getObjPositionInParent",
                    )
                    return
            return

        # Get the active journals for this scenario and document pool
        scenarios = getScenariosForCurrentUser()
        dp = self.context.myDocumentPool()
        # User could select more than one scenario
        for brain in api.content.find(
            context=dp,
            UID=scenarios,
        ):
            if not IArchiving(brain).is_archive:
                yield from api.content.find(
                    portal_type="Journal",
                    path=brain.getPath(),
                    sort_on="getObjPositionInParent",
                )


class AddForm(base.NullAddForm):
    def create(self):
        return Assignment()

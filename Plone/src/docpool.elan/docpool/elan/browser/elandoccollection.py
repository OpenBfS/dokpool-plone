from docpool.elan.browser.viewlets.common import EventViewlet
from docpool.elan.utils import getAvailableCategories
from docpool.elan.utils import getCategoriesForCurrentUser
from plone.base.utils import safe_text
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ELANDocCollectionView(BrowserView):
    """Default view"""

    __call__ = ViewPageTemplateFile("elandoccollection.pt")


class ELANDocCollectionrpopupView(BrowserView):
    """Additional View"""

    __call__ = ViewPageTemplateFile("elandoccollectionrpopup.pt")

    def selected_categories(self):
        """ """
        return getCategoriesForCurrentUser(self.context)

    def available_categories(self):
        """ """
        return [
            safe_text(brain.Title) for brain in getAvailableCategories(self.context)
        ]

    def scenario_view(self):
        """ """
        v = EventViewlet(self.context, self.request, self)
        v.update()
        return v


class ELANDocCollectionDocView(BrowserView):
    """Default view"""

    __call__ = ViewPageTemplateFile("elandoccollectiondoc.pt")

    def doc(self):
        """
        Return the elan document, which is to be viewed in the context of the collection.
        """
        uid = self.request.get("d", None)
        if uid:
            catalog = getToolByName(self, "portal_catalog")
            result = catalog({"UID": uid})
            if len(result) == 1:
                o = result[0].getObject()
                return o
        return None

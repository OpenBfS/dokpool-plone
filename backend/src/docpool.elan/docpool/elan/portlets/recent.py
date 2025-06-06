from AccessControl.SecurityInfo import allow_class
from AccessControl.SecurityInfo import allow_module
from Acquisition import aq_inner
from docpool.base.content.archiving import IArchiving
from docpool.elan import DocpoolMessageFactory as _
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer


# This interface defines the configurable options (if any) for the portlet.
# It will be used to generate add and edit forms. In this case, we don't
# have an edit form, since there are no editable options.


class IRecentPortlet(IPortletDataProvider):
    pass


# The assignment is a persistent object used to store the configuration of
# a particular instantiation of the portlet.


@implementer(IRecentPortlet)
class Assignment(base.Assignment):
    @property
    def title(self):
        return _("Recent")


# The renderer is like a view (in fact, like a content provider/viewlet). The
# item self.data will typically be the assignment (although it is possible
# that the assignment chooses to return a different object - see
# base.Assignment).


class Renderer(base.Renderer):
    # render() will be called to render the portlet

    render = ViewPageTemplateFile("recent.pt")

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        context = aq_inner(self.context)
        try:
            self.collection = (
                context.esd.recent
            )  # Acquire ELANCollection for recent documents
        except BaseException:
            self.collection = None

    @property
    def available(self):
        return (
            self.collection is not None
            and not IArchiving(self.context).is_archive
            and hasattr(self.context, "myELANCurrentSituation")
            and not self.isEditMode()
        )

    def recent_items(self):
        return self._data()

    def recently_modified_link(self):
        return self.collection.absolute_url()

    def isEditMode(self):
        """ """
        path = self.request.get("PATH_INFO", "")
        if path.endswith("/edit") or path.endswith("/@@edit"):
            return True

    def get_obj_url(self, brain):
        url = brain.getURL()
        if url.startswith("http"):
            # External links
            return url
        if getattr(self.context, "myDocumentPool", None) is None:
            # We're not within a dokpool
            print(url)
            return url
        dp_url = self.context.myDocumentPool().absolute_url()
        return f"{dp_url}/{url}"

    @memoize
    def _data(self):
        try:
            return self.collection.results(
                batch=True, b_start=0, b_size=5, sort_on=None, brains=True
            )
        except BaseException:
            return []


class AddForm(base.NullAddForm):
    # This method must be implemented to actually construct the object.

    def create(self):
        return Assignment()


allow_module("docpool.base.portlets")
allow_module("docpool.base.portlets.recent")
allow_class(Renderer)

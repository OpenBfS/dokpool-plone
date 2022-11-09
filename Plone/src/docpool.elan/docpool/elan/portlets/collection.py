from docpool.base.content.archiving import IArchiving
from docpool.base.utils import getDocumentPoolSite
from elan.esd import DocpoolMessageFactory as _
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import field
from zope import schema
from zope.interface import implementer


# This interface defines the configurable options (if any) for the portlet.
# It will be used to generate add and edit forms. In this case, we don't
# have an edit form, since there are no editable options.


class ICollectionPortlet(IPortletDataProvider):
    collection = schema.Choice(
        title=_("label_elandocument_doctype", default="Document Type"),
        description=_("description_elandocument_doctype", default=""),
        required=True,
        vocabulary="elan.esd.vocabularies.Category",
    )


# The assignment is a persistent object used to store the configuration of
# a particular instantiation of the portlet.


@implementer(ICollectionPortlet)
class Assignment(base.Assignment):
    def __init__(self, collection=None):
        self.collection = collection

    @property
    def title(self):
        return _("Collection")


# The renderer is like a view (in fact, like a content provider/viewlet). The
# item self.data will typically be the assignment (although it is possible
# that the assignment chooses to return a different object - see
# base.Assignment).


class Renderer(base.Renderer):

    # render() will be called to render the portlet

    render = ViewPageTemplateFile("collection.pt")

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        self.collection_id = self.data.collection
        esd = getDocumentPoolSite(self.context)
        path = "/".join(esd.getPhysicalPath()) + "/esd"
        cat = getToolByName(esd, "portal_catalog", None)
        items = cat(
            {
                "portal_type": "ELANDocCollection",
                "path": path,
                "getId": self.collection_id,
            }
        )
        if len(items) == 1:
            self.collection = items[0].getObject()
        else:
            self.collection = None

    @property
    def available(self):
        return self.collection is not None and not IArchiving(self.context).is_archive

    def recent_items(self):
        return self._data()

    def collection_link(self):
        return self.collection.absolute_url()

    def title(self):
        return self.collection and self.collection.Title() or "<no collection>"

    @memoize
    def _data(self):
        try:
            return self.collection.results(
                batch=True, b_start=0, b_size=10, sort_on=None, brains=True
            )
        except BaseException:
            return []


class AddForm(base.AddForm):
    form_fields = field.Fields(ICollectionPortlet)
    label = _("Add Collection Portlet")
    description = _(
        "This portlet displays recently modified content from a collection."
    )

    def create(self, data):
        return Assignment(collection=data.get("collection", None))


class EditForm(base.EditForm):
    form_fields = field.Fields(ICollectionPortlet)
    label = _("Edit Collection Portlet")
    description = _(
        "This portlet displays recently modified content from a collection."
    )

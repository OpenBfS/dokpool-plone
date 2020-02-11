from docpool.base.utils import extendOptions
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api

class CollectionDocView(BrowserView):
    """Default view
    """

    __call__ = ViewPageTemplateFile('collectiondoc.pt')

    def doc(self):
        """
        Return the document, which is to be viewed in the context of the collection.
        """
        uid = self.request.get("d", None)
        if uid:
            catalog = getToolByName(self, 'portal_catalog')
            result = catalog({'UID': uid})
            if len(result) == 1:
                o = result[0].getObject()
                return o
        return None

    def doc_inline(self):
        doc = self.doc()
        if doc:
            view = api.content.get_view(
                name='inline',
                context=doc,
                request=self.request,
            )
            return view()


class CollectionlistitemView(BrowserView):
    """Additional View
    """

    __call__ = ViewPageTemplateFile('collectionlistitem.pt')

    def options(self):
        return extendOptions(self.context, self.request, {})

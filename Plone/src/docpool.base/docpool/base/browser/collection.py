# -*- coding: utf-8 -*-
from docpool.base.browser.folderbase import FolderBaseView
from docpool.base.utils import extendOptions
from plone import api
from plone.app.contenttypes.browser.collection import CollectionView as BaseView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.i18n import translate


class CollectionView(BaseView):

    def __init__(self, context, request):
        # set batch size in request to fool the macro 'listing' from dp_macros.pt
        super(CollectionView, self).__init__(context, request)
        self.request.set('b_size', self.b_size)

    def getFolderContents(self, kwargs):
        # since we use the same template as for folders we need to get cintent differently
        return self.results()

    def dp_buttons(self, items):
        """
        Use the same method as for folder.
        """
        folderbaseview = FolderBaseView(self.context, self.request)
        return folderbaseview.dp_buttons(items)


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

    def translate_wf_action(self, doc, wf_action):
        translation_domain = 'docpool.base'
        actionhelpers = api.content.get_view(
            name='actionhelpers',
            context=doc,
            request=self.request,
        )
        if actionhelpers.is_rei_workflow(doc):
            translation_domain = 'docpool.rei'
        wf_state = wf_action['title']
        return translate(wf_state, domain=translation_domain, context=self.request)


class CollectionlistitemView(BrowserView):
    """Additional View
    """

    __call__ = ViewPageTemplateFile('collectionlistitem.pt')

    def options(self):
        return extendOptions(self.context, self.request, {})

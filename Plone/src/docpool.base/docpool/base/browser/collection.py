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
    """This view is @@docpool_collection_view_with_actions uses
    the template and class of FolderBaseView to display collections
    with checkboxes and buttons to trigger bulk-actions.
    """

    def __init__(self, context, request):
        super(CollectionView, self).__init__(context, request)
        # set batch size in request to fool the macro 'listing' from dp_macros.pt
        self.request.set('b_size', self.b_size)

    def getFolderContents(self, kwargs):
        """Since we use a template intended for folders we need to get content
        differently.
        """
        return self.results()

    def dp_buttons(self, items):
        """Get buttons from FolderBaseView but drop copy, cut and paste.
        """
        folderbaseview = FolderBaseView(self.context, self.request)
        folder_buttons = folderbaseview.dp_buttons(items)
        drop = ['copy', 'paste', 'cut']
        collection_buttons = [i for i in folder_buttons if i['id'] not in drop]
        return collection_buttons


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

    def _translation_domain(self, doc):
        actionhelpers = api.content.get_view(
            name='actionhelpers',
            context=doc,
            request=self.request,
        )
        if actionhelpers.is_rei_workflow(doc):
            return 'docpool.rei'
        return 'docpool.base'

    def translate_wf_action(self, doc, wf_action):
        translation_domain = self._translation_domain(doc)
        wf_state = wf_action['title']
        return translate(wf_state, domain=translation_domain, context=self.request)

    def wf_state(self, doc):
        translation_domain = self._translation_domain(doc)
        state = api.content.get_state(self.context, 'unknown')
        if state == 'unknown':
            title = 'Unknown'
        else:
            wf_tool = api.portal.get_tool('portal_workflow')
            title = wf_tool.getTitleForStateOnType(state, doc.portal_type)
        title = translate(title, domain=translation_domain, context=self.request)
        return dict(id=state, title=title)


class CollectionlistitemView(BrowserView):
    """Additional View
    """

    __call__ = ViewPageTemplateFile('collectionlistitem.pt')

    def options(self):
        return extendOptions(self.context, self.request, {})

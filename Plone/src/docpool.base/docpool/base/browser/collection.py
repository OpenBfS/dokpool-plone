# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
<<<<<<< HEAD
from plone import api
=======
from docpool.base.utils import extendOptions
from plone import api
from zope.i18n import translate

>>>>>>> Add i18n base / rei switch and translations

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

    def is_rei_workflow(self, doc):
        wf_tool = api.portal.get_tool('portal_workflow')
        workflow = wf_tool.getWorkflowsFor(doc)[0]
        rei_wfs = ['rei_review_workflow_alternative', 'rei_review_workflow_standard']
        import pdb; pdb.set_trace()
        if workflow.id in rei_wfs:
            return True
        return False

    def translate_wf_action(self, doc, wf_action):
        translation_domain = 'docpool.base'
        if self.is_rei_workflow(doc):
            translation_domain = 'docpool.rei'
        wf_state = wf_action['title']
        return translate(wf_state, domain=translation_domain, context=self.request)


class CollectionlistitemView(BrowserView):
    """Additional View
    """

    __call__ = ViewPageTemplateFile('collectionlistitem.pt')

    def options(self):
        return extendOptions(self.context, self.request, {})

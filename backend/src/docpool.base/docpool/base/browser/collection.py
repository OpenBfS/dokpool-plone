from docpool.base.browser.folderbase import FolderBaseView
from docpool.base.utils import extendOptions
from docpool.base.utils import is_rei_workflow
from plone import api
from plone.app.contenttypes.browser.collection import (
    CollectionView as CollectionBaseView,
)
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.i18n import translate


class CollectionView(CollectionBaseView):
    """This view is @@docpool_collection_view_with_actions uses
    the template and class of FolderBaseView to display collections
    with checkboxes and buttons to trigger bulk-actions.
    """

    def __init__(self, context, request):
        super().__init__(context, request)
        # set batch size in request to fool the macro 'listing' from dp_macros.pt
        self.request.set("b_size", self.b_size)

    def getFolderContents(self, kwargs):
        """Since we use a template intended for folders we need to get content
        differently.
        """
        return self.results()

    def dp_buttons(self, items):
        """Get buttons from FolderBaseView but drop copy, cut and paste."""
        folderbaseview = FolderBaseView(self.context, self.request)
        folder_buttons = folderbaseview.dp_buttons(items)
        drop = ["copy", "paste", "cut"]
        return [i for i in folder_buttons if i["id"] not in drop]


class CollectionDocView(BrowserView):
    """Default view"""

    __call__ = ViewPageTemplateFile("collectiondoc.pt")

    def doc(self):
        """
        Return the document, which is to be viewed in the context of the collection.
        """
        uid = self.request.get("d", None)
        if uid:
            return api.content.get(UID=uid)
        return None

    def doc_inline(self):
        doc = self.doc()
        if doc:
            view = api.content.get_view(
                name="inline",
                context=doc,
                request=self.request,
            )
            return view()

    def _translation_domain(self, doc):
        return "docpool.rei" if is_rei_workflow(doc) else "docpool.base"

    def translate_wf_action(self, doc, wf_action):
        translation_domain = self._translation_domain(doc)
        wf_state = wf_action["title"]
        return translate(wf_state, domain=translation_domain, context=self.request)

    def wf_state(self, doc):
        translation_domain = self._translation_domain(doc)
        state = api.content.get_state(doc, "unknown")
        if state == "unknown":
            title = "Unknown"
        else:
            wf_tool = api.portal.get_tool("portal_workflow")
            workflow = wf_tool.getWorkflowsFor(doc)[0]
            state_def = getattr(workflow.states, state, None)
            title = state_def.title if state_def is not None else state
        title = translate(title, domain=translation_domain, context=self.request)
        return dict(id=state, title=title)


class CollectionlistitemView(BrowserView):
    """Additional View"""

    __call__ = ViewPageTemplateFile("collectionlistitem.pt")

    def options(self):
        return extendOptions(self.context, self.request, {})


class DashboardCollectionView(CollectionBaseView):
    """This view is @@docpool_collection_view_with_actions_for_dashboardcollections
    It uses the template and class of FolderBaseView to display collections
    with checkboxes and buttons to trigger bulk-actions.
    """

    def __init__(self, context, request):
        super().__init__(context, request)
        # set batch size in request to fool the macro 'listing' from dp_macros.pt
        self.request.set("b_size", self.b_size)

    def getFolderContents(self, kwargs):
        """Since we use a template intended for folders we need to get content
        differently.
        """
        # Inject b_start since the DashboardCollection ignores the request - duh!
        results = self.context.results(b_start=self.request.get("b_start", 0))
        return results

    def dp_buttons(self, items):
        """Get buttons from FolderBaseView but drop copy, cut and paste."""
        folderbaseview = FolderBaseView(self.context, self.request)
        folder_buttons = folderbaseview.dp_buttons(items)
        drop = ["copy", "paste", "cut"]
        return [i for i in folder_buttons if i["id"] not in drop]

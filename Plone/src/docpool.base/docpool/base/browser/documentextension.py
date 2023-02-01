from docpool.base.appregistry import appIcon
from docpool.base.utils import getActiveAllowedPersonalBehaviorsForDocument
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DocMetaView(BrowserView):
    """Default view"""

    __call__ = ViewPageTemplateFile("doc_meta.pt")

    def meta_infos(self):
        context = self.context
        portal_state = api.content.get_view("plone_portal_state", context, self.request)
        portal_url = portal_state.portal_url()
        behavior_names = getActiveAllowedPersonalBehaviorsForDocument(
            context, self.request
        )
        results = []
        for behavior_name in behavior_names:
            icon = appIcon(behavior_name)
            item = {
                "behavior_name": behavior_name,
                "icon_url": icon and f"{portal_url}/{icon}" or False,
                "behavior": context.doc_extension(behavior_name),
            }
            # TODO: Sort?
            results.append(item)
        return results


class DocActionsView(BrowserView):
    """Default view"""

    __call__ = ViewPageTemplateFile("doc_actions.pt")

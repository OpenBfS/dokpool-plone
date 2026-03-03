from docpool.base.behaviors.transferable import ITransferable
from docpool.base.behaviors.utils import allowed_targets
from docpool.base.config import FOLDER_TYPES
from docpool.base.config import OTHER_TYPES
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.utils import get_current_state_title
from docpool.ui import _
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import queryUtility


TRANSITION_ICON_MAPPING = {
    "publish": "eye",
    "reject_second": "box-arrow-in-left",
    "reject_to_authority": "box-arrow-in-left",
    "reject_to_bfs": "box-arrow-in-left",
    "reject_to_npp_operator": "box-arrow-in-left",
    "reject": "box-arrow-in-left",
    "retract_for_revision": "box-arrow-in-left",
    "retract_to_authority": "box-arrow-in-left",
    "retract_to_bfs": "box-arrow-in-left",
    "retract_to_npp_operator": "box-arrow-in-left",
    "retract": "eye-slash",
    "submit_authority": "arrow-right",
    "submit_bfs": "arrow-right",
    "submit_bmu": "arrow-right",
    "submit_second": "arrow-right",
    "submit": "arrow-right",
}


class Item(BrowserView):
    template = ViewPageTemplateFile("templates/listing-item.pt")
    template_folder = ViewPageTemplateFile("templates/listing-folder.pt")
    template_other = ViewPageTemplateFile("templates/listing-other.pt")

    def __call__(self, uid=None):
        obj = api.content.get(UID=uid) if uid else self.context

        if obj.portal_type == "DPDocument":
            return self.prepare_entry(obj)
        if obj.portal_type in FOLDER_TYPES:
            return self.prepare_folder(obj)
        return self.prepare_other(obj)

    def prepare_entry(self, obj):
        review_state = api.content.get_state(obj)
        review_state_title = get_current_state_title(obj, review_state)

        idnormalizer = queryUtility(IIDNormalizer)
        state_class = f"state-{idnormalizer.normalize(review_state)}"
        portal_workflow = api.portal.get_tool("portal_workflow")
        available_transitions = portal_workflow.getTransitionsFor(obj)

        modified_by_user = ""
        modified_by_group = ""
        if userinfo := obj.modified_by or obj.created_by:
            modified_by_user = userinfo[1]
            modified_by_group = userinfo[2]

        show_transfer_action = False
        if api.user.has_permission("Docpool: Send Content", obj=obj):
            try:
                adapted = ITransferable(obj)
            except TypeError:
                pass
            else:
                if adapted.transferable() and allowed_targets(obj):
                    show_transfer_action = True

        icon_name = "question"  # Unknown type as fallback
        doctype_title = obj.docType  # id of initially selected DocType as fallback
        if docTypeObj := obj.docTypeObj():
            icon_name = docTypeObj.icon_name
            doctype_title = docTypeObj.title

        iconresolver = self.context.restrictedTraverse("@@iconresolver")
        attachments = api.content.get_view("contentlisting", obj, self.request)(portal_type=["Image", "File"])

        self.dpdocument = {
            "date": obj.mdate,
            "title": obj.title,
            "id": obj.id,
            "description": obj.description,
            "review_state": review_state,
            "state_title": review_state_title,
            "state_class": state_class,
            "available_transitions": available_transitions,
            "uid": obj.UID(),
            "doctype": obj.docType,
            "doctype_title": doctype_title,
            "doctype_icon_url": iconresolver.url(icon_name),
            "url": obj.absolute_url(),
            "path": obj.absolute_url_path(),
            "modified_by_user": modified_by_user,
            "modified_by_group": modified_by_group,
            "show_transfer_action": show_transfer_action,
            "attachments": attachments,
        }
        return self.index()

    def transition_icon(self, transition_id):
        return TRANSITION_ICON_MAPPING.get(transition_id, "arrow-right")

    def mimetype_name(self, content_type):
        mtr = api.portal.get_tool("mimetypes_registry")
        mimetypes = mtr.lookup(content_type)
        return mimetypes[0].name() if mimetypes else content_type.split("/")[-1]

    def prepare_folder(self, obj):
        modified_by_user = ""
        modified_by_group = ""
        if userinfo := getattr(obj, "modified_by", None) or getattr(obj, "created_by", None):
            modified_by_user = userinfo[1]
            modified_by_group = userinfo[2]

        iconresolver = self.context.restrictedTraverse("@@iconresolver")
        icon_name = "folder"
        count = len(obj.contentItems())
        self.folder = {
            "date": getattr(obj, "mdate", None),
            "title": obj.title,
            "id": obj.id,
            "description": obj.description,
            "doctype": obj.portal_type,
            "doctype_title": obj.portal_type,
            "doctype_icon_url": iconresolver.url(icon_name),
            "uid": obj.UID(),
            "icon": iconresolver.url(icon_name),
            "url": obj.absolute_url(),
            "path": obj.absolute_url_path(),
            "modified_by_user": modified_by_user,
            "modified_by_group": modified_by_group,
            "count": count,
        }
        return self.template_folder()

    def prepare_other(self, obj):
        modified_by_user = ""
        modified_by_group = ""
        if userinfo := getattr(obj, "modified_by", None) or getattr(obj, "created_by", None):
            modified_by_user = userinfo[1]
            modified_by_group = userinfo[2]

        iconresolver = self.context.restrictedTraverse("@@iconresolver")
        icon_name = "document"
        self.folder = {
            "date": getattr(obj, "mdate", None),
            "title": obj.title,
            "id": obj.id,
            "description": obj.description,
            "doctype": obj.portal_type,
            "doctype_title": obj.portal_type,
            "doctype_icon_url": iconresolver.url(icon_name),
            "uid": obj.UID(),
            "icon": iconresolver.url(icon_name),
            "url": obj.absolute_url(),
            "path": obj.absolute_url_path(),
            "modified_by_user": modified_by_user,
            "modified_by_group": modified_by_group,
        }
        return self.template_other()

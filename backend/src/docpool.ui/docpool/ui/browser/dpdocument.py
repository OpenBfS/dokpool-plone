from docpool.base.behaviors.transferable import ITransferable
from docpool.base.behaviors.utils import allowed_targets
from docpool.base.browser.dpdocument import DPDocumentEditForm
from docpool.base.content.groupfolder import IGroupFolder
from docpool.base.content.places import IPlaces
from docpool.base.utils import getDocumentPoolSite
from docpool.base.utils import getUserInfo
from docpool.ui import _
from docpool.ui.utils import prepare_came_from_link
from plone import api
from plone.app.content.browser.actions import DeleteConfirmationForm
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.interfaces import IDexterityEditForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import button
from zope.interface import implementer

import io
import zipfile


class DPDocumentView(DefaultView):
    """View for all DPDocuments."""

    def __call__(self):
        if "download_attachments" in self.request.form:
            return self.download_attachments()

        self.event = api.content.get(UID=uid) if (uid := getattr(self.context, "scenario", None)) else None
        self.group_folder = api.content.get_closest_ancestor(self.context, interface=IGroupFolder)
        return super().__call__()

    def download_attachments(self):
        """Creates a zip file containing all attachments and returns it for download."""
        contentlisting = self.context.restrictedTraverse("@@contentlisting")
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for item in contentlisting(portal_type=["Image", "File"]):
                obj = item.getObject()
                # Handle file and image fields
                data_attr = obj.portal_type.lower()
                if data := getattr(obj.aq_base, data_attr, None):
                    # Add file to ZIP
                    zip_file.writestr(data.filename, data.data)

        # Reset zipfile-buffer
        zip_buffer.seek(0)
        self.request.response.setHeader("Content-Type", "application/zip")
        self.request.response.setHeader(
            "Content-Disposition", f'attachment; filename="{self.context.id}_attachments.zip"'
        )
        return zip_buffer.read()

    def icon_name(self):
        return self.context.docTypeObj().icon_name

    def getDocpoolListingPath(self):
        dp = getDocumentPoolSite(self.context)
        path = "/".join(dp.getPhysicalPath()) + "/@@listing"
        return path

    def workflow_state(self):
        return api.content.get_state(self.context)

    def published_info(self):
        wftool = api.portal.get_tool("portal_workflow")
        if not (wfs := wftool.getWorkflowsFor(self.context)):
            return
        if not (history := wftool.getHistoryOf(wfs[0].id, self.context)):
            return
        if (last := history[-1])["review_state"] != "published":
            return
        return last["time"], self.context.formatUserInfo(getUserInfo(self.context, last["actor"]))

    @property
    def show_transfer_action(self):
        if api.user.has_permission("Docpool: Send Content", obj=self.context):
            try:
                adapted = ITransferable(self.context)
            except TypeError:
                pass
            else:
                if adapted.transferable() and allowed_targets(self.context):
                    return True

    def visibility_options(self):
        dp_app_state = api.content.get_view("dp_app_state", self.context, self.request)
        app = dp_app_state.appsActivatedByCurrentUser()[0]
        return {
            o["value"]: o
            for o in visibility_options(
                app,
                self.group_folder if self.group_folder is not None else self.context,
            )
        } | {
            "pending": {"title": _("Pending")},
            "revised": {"title": _("Revised")},
        }


def visibility_options(app, context):
    options = []
    if IGroupFolder.providedBy(context):
        group_title = context.title
        options.append({
            "value": "private",
            "title": _("Internal"),
            "description": _(
                "Only for member of '${container_title}'", mapping={"container_title": group_title}
            ),
        })
    docpool_title = IPlaces(context).document_pool.title
    options.extend([
        {
            "value": "published",
            "title": _("Published"),
            "description": _(
                "For all users of '${app} ${docpool_title}'",
                mapping={"app": app.upper(), "docpool_title": docpool_title},
            ),
        },
    ])
    return options


@implementer(IDexterityEditForm)
class DPDocumentEditFormUI(DPDocumentEditForm):
    """Edit view for all DPDocuments."""

    template = ViewPageTemplateFile("templates/dpdocument-edit.pt")
    enable_form_tabbing = False

    def render(self):
        self.title_widget = self.widgets.pop("IDublinCore.title", None)
        self.text_widget = self.widgets.pop("text", None)
        return super().render()


class DPDocumentDeleteConfirmationFormUI(DeleteConfirmationForm):
    """Override to add our custom redirect."""

    template = ViewPageTemplateFile("templates/delete_confirmation.pt")

    @button.buttonAndHandler(_("Delete"), name="Delete")
    def handle_delete(self, action):
        listing_url = prepare_came_from_link(self.request)
        super().handle_delete(self, action)

        if listing_url:
            self.request.response.redirect(listing_url)
        else:
            self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_("label_cancel", default="Cancel"), name="Cancel")
    def handle_cancel(self, action):

        listing_url = prepare_came_from_link(self.request)
        if listing_url:
            self.request.response.redirect(listing_url)
        else:
            self.request.response.redirect(self.context.absolute_url())

    def updateActions(self):
        super().updateActions()

        # Pass it as hidden input in delete_confirm template so we can use it in the buttonHandler
        if "came_from" in self.request:
            self.came_from = self.request.get("came_from")

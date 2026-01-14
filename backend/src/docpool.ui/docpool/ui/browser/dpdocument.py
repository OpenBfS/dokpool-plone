from docpool.base import DocpoolMessageFactory as _
from docpool.base.appregistry import APP_REGISTRY
from docpool.base.browser.dpdocument import DPDocumentEditForm
from docpool.base.utils import getDocumentPoolSite
from docpool.ui.utils import prepare_came_from_link
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

        return super().__call__()

    def apps(self):
        results = {}
        for app in APP_REGISTRY:
            if app in self.context.local_behaviors:
                results[app] = self.context.doc_extension(app)
        return results

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


@implementer(IDexterityEditForm)
class DPDocumentEditFormUI(DPDocumentEditForm):
    """Edit view for all DPDocuments."""

    template = ViewPageTemplateFile("templates/dpdocument-edit.pt")
    enable_form_tabbing = False

    def render(self):
        self.text_widget = self.widgets.pop("text", None)
        self.description_widget = self.widgets.pop("IDublinCore.description", None)
        return super().render()


class DPDocumentDeleteConfirmationFormUI(DeleteConfirmationForm):
    """Override to add our custom redirect."""

    template = ViewPageTemplateFile("templates/delete_confirmation.pt")

    @button.buttonAndHandler(_("Delete"), name="Delete")
    def handle_delete(self, action):
        super().handle_delete(self, action)

        listing_url = prepare_came_from_link(self.request)
        self.request.response.redirect(listing_url + "/@@listing")

    @button.buttonAndHandler(_("label_cancel", default="Cancel"), name="Cancel")
    def handle_cancel(self, action):

        listing_url = prepare_came_from_link(self.request)
        self.request.response.redirect(listing_url + "/@@listing")

    def updateActions(self):
        super().updateActions()

        # Pass it as hidden input in delete_confirm template so we can use it in the buttonHandler
        if "came_from" in self.request:
            self.came_from = self.request.get("came_from")

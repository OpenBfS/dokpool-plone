from docpool.base.appregistry import APP_REGISTRY
from docpool.base.browser.dpdocument import DPDocumentEditForm
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.interfaces import IDexterityEditForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
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


@implementer(IDexterityEditForm)
class DPDocumentEditFormUI(DPDocumentEditForm):
    """Edit view for all DPDocuments."""

    template = ViewPageTemplateFile("templates/dpdocument-edit.pt")
    enable_form_tabbing = False

    def updateWidgets(self):
        super().updateWidgets()
        self.text_widget = self.widgets.pop("text", None)
        self.description_widget = self.widgets.pop("IDublinCore.description", None)

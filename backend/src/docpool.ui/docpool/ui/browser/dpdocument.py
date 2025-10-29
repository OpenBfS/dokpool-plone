from docpool.base.appregistry import APP_REGISTRY
from docpool.ui.browser.listing import DOCTYPE_ICON_MAPPING
from plone.dexterity.browser.view import DefaultView

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

    def doctype_icon(self, doctype):
        return DOCTYPE_ICON_MAPPING.get(doctype, "radioactive")

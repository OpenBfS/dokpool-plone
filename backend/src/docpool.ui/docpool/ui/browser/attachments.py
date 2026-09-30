from docpool.base.preview import ANNOTATION_KEY
from plone import api
from plone.base.utils import human_readable_size
from Products.Five.browser import BrowserView
from urllib.parse import urlencode
from zope.annotation import IAnnotations


class Attachments(BrowserView):
    def items(self):
        contentlisting = self.context.restrictedTraverse("@@contentlisting")
        return contentlisting(portal_type=["File", "Image"])

    def can_reorder(self):
        return api.user.has_permission("Modify portal content", obj=self.context)

    def can_delete(self, item):
        return api.user.has_permission("Delete objects", obj=item.getObject())

    def delete_confirmation_url(self, item):
        query = urlencode({"came_from": f"{self.context.absolute_url()}/edit"})
        return f"{item.getURL()}/@@attachment_delete_confirmation?{query}"

    def total_size(self):
        sizes = [i.getSize() for i in self.items()]
        complete = complete_size_in_bytes(sizes)
        return human_readable_size(complete)

    def mimetype_name(self, content_type):
        mtr = api.portal.get_tool("mimetypes_registry")
        mimetypes = mtr.lookup(content_type)
        return mimetypes[0].name() if mimetypes else content_type.split("/")[-1]

    def pages(self, obj):
        annotations = IAnnotations(obj)
        previews = annotations.get(ANNOTATION_KEY, None)
        if previews and "pages" in previews:
            return previews["pages"]


def complete_size_in_bytes(values):
    """Calculate total sum of sizes ["1.2 KB", "2 MB"] as stored on brains."""
    SIZE_CONST = {
        "B": 1,
        "KB": 1024,
        "MB": 1024**2,
        "GB": 1024**3,
        "TB": 1024**4,
        "PB": 1024**5,
    }
    total_bytes = 0
    for v in values:
        if not v:
            continue
        num, unit = v.strip().split()
        num = float(num.replace(",", "."))
        total_bytes += num * SIZE_CONST[unit.upper()]
    return total_bytes

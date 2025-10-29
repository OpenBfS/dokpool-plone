from plone import api
from plone.base.utils import human_readable_size
from Products.Five.browser import BrowserView


class Attachments(BrowserView):
    def items(self):
        contentlisting = self.context.restrictedTraverse("@@contentlisting")
        return contentlisting(portal_type=["File", "Image"])

    def total_size(self):
        sizes = [i.getSize() for i in self.items()]
        complete = complete_size_in_bytes(sizes)
        return human_readable_size(complete)

    def mimetype_name(self, content_type):
        mtr = api.portal.get_tool("mimetypes_registry")
        mimetypes = mtr.lookup(content_type)
        return mimetypes[0].name() if mimetypes else content_type.split("/")[-1]


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

from Products.Five import BrowserView


class ContextHelpers(BrowserView):
    """Stuff that previously were skin scripts"""

    def is_archive(self):
        return "archive" in self.context.getPhysicalPath()

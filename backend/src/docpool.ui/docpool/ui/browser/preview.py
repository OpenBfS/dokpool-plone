from docpool.base.preview import ANNOTATION_KEY
from Products.Five.browser import BrowserView
from zope.annotation import IAnnotations


class Preview(BrowserView):
    def __call__(self, scale="1200"):
        annotations = IAnnotations(self.context)
        if previews := annotations.get(ANNOTATION_KEY, None) is None:
            return
        self.request.response.setHeader("Content-Type", "image/jpeg")
        return self.request.response.write(previews[scale])

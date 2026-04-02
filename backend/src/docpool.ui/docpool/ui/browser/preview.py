from docpool.base.preview import ANNOTATION_KEY
from plone.namedfile.file import NamedBlobImage
from plone.namedfile.utils import set_headers
from plone.namedfile.utils import stream_data
from Products.Five.browser import BrowserView
from zope.annotation import IAnnotations


class Preview(BrowserView):
    def __call__(self, scale="great"):
        annotations = IAnnotations(self.context)
        if (previews := annotations.get(ANNOTATION_KEY, None)) is None:
            return
        image = previews.get(scale, None)
        if not isinstance(image, NamedBlobImage):
            return
        # Setting a filename forced download
        set_headers(image, self.request.response, filename=None)
        return stream_data(image)

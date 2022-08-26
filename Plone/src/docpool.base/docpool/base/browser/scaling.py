from Acquisition import aq_base
from logging import exception
from plone.namedfile.file import FileChunk
from plone.namedfile.interfaces import IStableImageScale
from plone.namedfile.scaling import (
    DefaultImageScalingFactory as OriginalImageScalingFactory,
)
from plone.namedfile.scaling import ImageScale
from plone.namedfile.scaling import ImageScaling as OriginalImageScaling
from plone.scale.scale import scaleImage
from plone.scale.storage import AnnotationStorage
from Products.CMFPlone.utils import safe_callable
from ZODB.POSException import ConflictError
from zope.interface import alsoProvides
from zope.publisher.interfaces import NotFound

import logging


_marker = object()


logger = logging.getLogger(__name__)


class ImageScaling(OriginalImageScaling):
    """view used for generating (and storing) image scales"""

    def publishTraverse(self, request, name):
        """used for traversal via publisher, i.e. when using as a url"""
        stack = request.get("TraversalRequestNameStack")
        image = None
        if stack:
            # field and scale name were given...
            scale = stack.pop()
            image = self.scale(name, scale)  # this is aq-wrapped
        elif "-" in name:
            # we got a uid...
            if "." in name:
                name, ext = name.rsplit(".", 1)
            storage = AnnotationStorage(self.context)
            info = storage.get(name)
            if info is not None:
                scale_view = ImageScale(self.context, self.request, **info)
                alsoProvides(scale_view, IStableImageScale)
                return scale_view.__of__(self.context)
        else:
            # otherwise `name` must refer to a field...
            if "." in name:
                name, ext = name.rsplit(".", 1)
            value = getattr(self.context, name)

            # BfS extension:
            if callable(value):
                value = value()

            scale_view = ImageScale(
                self.context, self.request, data=value, fieldname=name
            )
            return scale_view.__of__(self.context)
        if image is not None:
            return image
        raise NotFound(self, name, self.request)

    def create(
        self, fieldname, direction="thumbnail", height=None, width=None, **parameters
    ):
        """factory for image scales, see `IImageScaleStorage.scale`"""
        orig_value = getattr(self.context, fieldname)

        # BfS extension:
        if callable(orig_value):
            orig_value = orig_value()

        if orig_value is None:
            return

        if height is None and width is None:
            _, format = orig_value.contentType.split("/", 1)
            return None, format, (orig_value._width, orig_value._height)
        if hasattr(aq_base(orig_value), "open"):
            orig_data = orig_value.open()
        else:
            orig_data = getattr(aq_base(orig_value), "data", orig_value)
        if not orig_data:
            return

        # Handle cases where large image data is stored in FileChunks instead
        # of plain string
        if isinstance(orig_data, FileChunk):
            # Convert data to 8-bit string
            # (FileChunk does not provide read() access)
            orig_data = str(orig_data)

        # If quality wasn't in the parameters, try the site's default scaling
        # quality if it exists.
        if "quality" not in parameters:
            quality = self.getQuality()
            if quality:
                parameters["quality"] = quality

        try:
            result = scaleImage(
                orig_data, direction=direction, height=height, width=width, **parameters
            )
        except (ConflictError, KeyboardInterrupt):
            raise
        except Exception:
            exception(
                'could not scale "%r" of %r', orig_value, self.context.absolute_url()
            )
            return
        if result is not None:
            data, format, dimensions = result
            mimetype = "image/%s" % format.lower()
            value = orig_value.__class__(
                data, contentType=mimetype, filename=orig_value.filename
            )
            value.fieldname = fieldname
            return value, format, dimensions


class ImageScalingFactory(OriginalImageScalingFactory):
    def __init__(self, context):
        self.context = context

    def __call__(
        self,
        fieldname=None,
        direction="thumbnail",
        height=None,
        width=None,
        scale=None,
        **parameters,
    ):
        """Factory for image scales`."""
        orig_value = getattr(self.context, fieldname, None)
        if not orig_value:
            return
        if safe_callable(orig_value):
            orig_value = orig_value()

        orig_data = getattr(aq_base(orig_value), "data", orig_value)

        # If quality wasn't in the parameters, try the site's default scaling
        # quality if it exists.
        if "quality" not in parameters:
            quality = self.get_quality()
            if quality:
                parameters["quality"] = quality

        try:
            result = self.create_scale(
                orig_data, direction=direction, height=height, width=width, **parameters
            )
        except (ConflictError, KeyboardInterrupt):
            raise
        except OSError:
            if getattr(orig_value, "contentType", "") == "image/svg+xml":
                result = orig_data.read(), "SVG", (width, height)
            else:
                logger.exception(
                    'Could not scale "{!r}" of {!r}'.format(
                        orig_value, self.context.absolute_url
                    )
                )
                return
        except Exception as e:
            logger.exception(
                'Could not scale "{!r}" of {!r}'.format(
                    orig_value, self.context.absolute_url
                )
            )
            return
        if result is None:
            return
        data, format_, dimensions = result
        mimetype = f"image/{format_.lower()}"
        value = orig_value.__class__(
            data, contentType=mimetype, filename=orig_value.filename
        )
        value.fieldname = fieldname
        return value, format_, dimensions

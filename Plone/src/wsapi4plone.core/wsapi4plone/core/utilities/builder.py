from zope.interface import implementer
from zope.publisher.interfaces import NotFound

from wsapi4plone.core.interfaces import IContextBuilder
import six


@implementer(IContextBuilder)
class Builder(object):

    def __call__(self, context, path):
        """
        @param context - fallback if path is 'None' or method of getting the object from the path
        @param path - string to the path of the wanted object
        """
        if not path:
            found_object = context
        elif isinstance(path, str) or isinstance(path, six.text_type):
            try:
                found_object = context.restrictedTraverse(path)
            except KeyError:
                raise NotFound(context, path)
        else:
            # path must be an object?
            found_object = path

        return found_object

    def get_path(self, context, path=''):
        physical_path = self.__call__(context, path).getPhysicalPath()
        return '/'.join(physical_path)


def builder():
    return Builder()

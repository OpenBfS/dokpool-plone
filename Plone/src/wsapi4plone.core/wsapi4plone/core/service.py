try:
    from zope.container.interfaces import IContainer
except ImportError:
    from zope.app.container.interfaces import IContainer
    
from zope.component import (adapts, getMultiAdapter, getUtilitiesFor,
    queryMultiAdapter)
from zope.interface import implements, implementsOnly, Interface

from wsapi4plone.core.interfaces import IService, IServiceContainer
from wsapi4plone.core.interfaces import IExtension, IServiceExtension


class Service(object):
    """The service base class."""
    adapts(Interface)
    implements(IService)

    def __init__(self, context):
        self.context = context

    def get_skeleton(self, filtr=[]):
        raise NotImplementedError(
            "%s does not implement the get_skeleton method. Attempting to " \
            "adapt %s." % (self.__class__.__name__, self.context))

    def get_object(self, attrs=[]):
        raise NotImplementedError(
            "%s does not implement the get_object method. Attempting to " \
            "adapt %s." % (self.__class__.__name__, self.context))

    def get_type(self):
        raise NotImplementedError(
            "%s does not implement the get_type method. Attempting to adapt " \
            "%s." % (self.__class__.__name__, self.context))

    def get_extensions(self, as_callback=False):
        misc = {}
        for name, iface in getUtilitiesFor(IServiceExtension):
            # print self, self.context, iface, name
            ext = queryMultiAdapter((self, self.context), iface,
                name=name)
            # print self.context, ext, name
            if ext:
                if as_callback and ext.provides_callback:
                    name = '%s.callback' % name
                    accessor = ext.get_callback
                else:
                    accessor = ext.get
                misc[name] = accessor()
        return misc

    get_misc = get_extensions # BBB

    def set_extensions(self, params={}):
        extensions = [(n,i,) for n,i in getUtilitiesFor(IServiceExtension)]
        extensions = dict(extensions)
        for ext_name, ext_params in params.iteritems():
            if ext_name in extensions.keys():
                ext = getMultiAdapter((self, self.context),
                    extensions[ext_name],
                    name=ext_name)
                ext.set(**ext_params)

    def set_properties(self, params):
        raise NotImplementedError(
            "%s does not implement the set_properties method. Attempting to " \
            "adapt %s." % (self.__class__.__name__, self.context))

    def clipboard(self, action, target, destination):
        raise NotImplementedError(
            "%s does not implement the clipboard method. Attempting to " \
            "adapt %s." % (self.__class__.__name__, self.context))


class ServiceContainer(Service):
    adapts(IContainer)
    implementsOnly(IServiceContainer)

    def delete_object(self, id_):
        raise NotImplementedError(
            "%s does not implement the delete_object method. Attempting to " \
            "adapt %s." % (self.__class__.__name__, self.context))

    def create_object(self, type_name, id_):
        raise NotImplementedError(
            "%s does not implement the create_object method. Attempting to " \
            "adapt %s." % (self.__class__.__name__, self.context))

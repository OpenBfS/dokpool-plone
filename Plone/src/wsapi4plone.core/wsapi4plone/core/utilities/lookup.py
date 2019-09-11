try:
    from zope.container.interfaces import IContainer
except ImportError:
    from zope.app.container.interfaces import IContainer
from zope.component import getUtility
from zope.interface import implementer

from wsapi4plone.core.interfaces import (
    IContextBuilder,
    IService,
    IServiceContainer,
    IServiceLookup,
)


@implementer(IServiceLookup)
class ServiceLookup(object):
    """
    Lookup a Service based on the path.

    First we need to setup the environment with example data.

        >>> from zope.app.container.sample import SampleContainer
        >>> from zope.location import Location
        >>> root = SampleContainer()
        >>> container = root['container'] = SampleContainer()
        >>> container['subcontainer'] = SampleContainer()
        >>> loc2 = container['subcontainer']['loc2'] = Location()

    Next let's just make a little function to generate the path for us.

        >>> from zope.location import LocationIterator
        >>> def getPath(object_):
        ...     results = []
        ...     for obj in LocationIterator(object_):
        ...         if not obj.__name__:
        ...             results.append('')
        ...         else:
        ...             results.append(obj.__name__)
        ...     results.reverse()
        ...     return u'/'.join(results)
        ...
        >>> getPath(loc2)
        u'/container/subcontainer/loc2'

    Now that we have a path we can hand it to the service lookup, but we will
    get a component lookup error for IContextBuilder. So, let's make a context
    builder.

        >>> def builder(context, path):
        ...     obj = context
        ...     for step in path:
        ...         if step == '':
        ...             continue
        ...         else:
        ...             obj = obj[step]
        ...     return obj
        >>> path = getPath(loc2).split('/')
        >>> builder(root, path).__name__
        u'loc2'

    Let's register the components needed by ServiceLookup, which are the
    context builder utility, a service adapter and a service container
    adapter.

        >>> from zope.app.testing import ztapi
        >>> from zope.interface import Interface
        >>> from zope.app.container.interfaces import IContainer
        >>> from wsapi4plone.core.interfaces import IContextBuilder, IService, IServiceContainer
        >>> from wsapi4plone.core.service import Service, ServiceContainer
        >>> ztapi.provideUtility(IContextBuilder, builder)
        >>> ztapi.provideAdapter(Interface, IService, Service)
        >>> ztapi.provideAdapter(IContainer, IServiceContainer, ServiceContainer)

    Finally, try the ServiceLookup.

        >>> from wsapi4plone.core.utilities.lookup import ServiceLookup
        >>> lookup = ServiceLookup()
        >>> serviced = lookup(root, path)
        >>> serviced.__class__.__name__
        'Service'
        >>> container_path = getPath(container['subcontainer']).split('/')
        >>> serviced_container = lookup(root, container_path)
        >>> serviced_container.__class__.__name__
        'ServiceContainer'

    """

    def __call__(self, context, path=''):
        builder = getUtility(IContextBuilder)
        obj = builder(context, path)
        if IContainer.providedBy(obj):
            return IServiceContainer(obj)
        else:
            return IService(obj)


def lookup():
    return ServiceLookup()

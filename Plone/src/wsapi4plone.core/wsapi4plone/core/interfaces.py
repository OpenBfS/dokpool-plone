from zope.interface.interfaces import IInterface
from zope.interface import Interface, Attribute

from wsapi4plone.core.utilities.interfaces import (IScrubber, IContextBuilder,
    IServiceLookup, IFormatQueryResults)


class IService(Interface):
    """Adapts an object to an XML-RPC compatible format."""

    def get_skeleton(filtr=[]):
        """Get a skeleton data structure of the object without its values."""

    def get_object(attrs=[]):
        """Represent the object in serviceable output. See this package's
        specification for further information on servicible output.
        """

    def get_type():
        """A type name representative of the type across the plone system. More
        importantly it should be the name proper name and not the user
        friendly name."""

    def get_misc(as_callback=False):
        """Get any miscellaneous data associated with the object (contents,
        computed results, etc.)
        """

    def set_misc(params):
        """Set any miscellaneous data associated with the object (contents,
        computed results, etc.)
        """

    def set_properties(params):
        """Given a dictionary of parameters, set_properities attempts to set
        the context's attributes with the data."""

    def clipboard(action, target, destination):
        """Clipboard actions... copy, cut and paste. paste is implied from
        either copy or cut action."""


class IServiceContainer(IService):

    def create_object(type_name, id_):
        """Create a child object of the parent object given the type_name and
        name it with id_."""

    def delete_object(id_):
        """Delete the child object from the id_ given. Returns True if the
        process was successful."""


class IServiceExtension(IInterface):
    """An IExtension registry."""


class IExtension(Interface):
    """An extension that adapts both a service and content object."""

    provides_callback = Attribute("Boolean value that defines whether"
                                  "this extension provides callback support.")

    def get():
        """Retrieves the extensions results."""


class IReadExtension(IExtension):
    """An extension that provides read-only functionality."""


class IWriteExtension(IReadExtension):
    """An extension that provides both read and write functionality."""

    def set(**kwargs):
        """Assigns values to the extension that can then be assigned to
        service adapter or contextual object."""

    def get_skeleton():
        """Provides a skeletonal structure for items that can be assigned
        (via the set method) to this extension."""


class ICallbackExtension(IReadExtension):
    """An exension provides callback functionality."""

    def get_callback():
        """Provides the callback version of an extensions get method."""

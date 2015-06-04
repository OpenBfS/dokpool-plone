from zope.interface.interfaces import IInterface
from zope.interface import Interface, Attribute


class IScrubber(Interface):
    """This utility is intended to scrub a data structure clean so that an
    can be marshalled for whatever web service is requesting the data
    structure."""

    def dict_scrub(data):
        """This method will clean a dictionary and bring any of its data types
        to the standard built-in types or types that are known to marshall.
        """


class IContextBuilder(Interface):
    """Builds the context from a given context (most likely the site) and
    string path."""


class IServiceLookup(Interface):
    """Finds an object from a context and string path and provides the Serviced
    object as its result."""


class IFormatQueryResults(Interface):
    """Given a list of brains, this utility will provide spec formatted output
    for a portal_catalog query."""

from zope.interface import Interface, Attribute


class IAPILayer(Interface):
    """Browser layer to enable and disable API calls."""


class ISystemAPI(Interface):
    """
    A specification for the XML-RPC Introspection protocol, found at
    (http://xmlrpc-c.sourceforge.net/introspection.html). XML-RPC
    Introspection is a facility of XML-RPC clients and servers that enables
    a client to learn from a server what XML-RPC methods it implements. 
    """

    spec_id = Attribute("The identification name of the specification.")
    spec_version = Attribute("A version number.")
    spec_url = Attribute("URL where the specification and detailed description can be found.")

    def get_capabilities():
        """
        get_capabilities specifies XML-RPC Introspection version 1
        (http://xmlrpc-c.sourceforge.net/introspection.html). This method is
        used to define the capabilites of the XML-RPC introspection. The
        specification states that get_capabilities should at the very least
        return the specification id, version and URL.
        """

    def method_signature(method_name):
        """
        method_signature returns a description of the argument format for
        the given method_name.
        """

    def list_methods():
        """
        list_methods returns a list of the methods the XML-RPC server
        implements.
        """

    def method_help(method_name):
        """
        method_help returns a text description for the given method_name.
        """

    def multicall():
        """multiple calls at once (boxcarring)"""


class IApplicationAPI(Interface):
    """
    Application specific API. The ApplicationAPI class is a collection of
    zope2 browser views that can be used to view, create and modify site objects.
    """

    def get_object(path='', attrs=[]):
        """get the raw data from an object (GET)"""

    def get_file_object(path='', attr=''):
        """ """

    def post_object(params, type_name, path=''):
        """
        Post or create an object with the name given in path of type.
        An 'id' must be given to create an object. The id can either be given
        via params or an extention of path (e.g. {'id': 'newid'} or
        /folder/subfolder/newid).
        The params keys can be made available via a call to get_schema(type="the type").
        The type_name parameter is a valid type that can be verified with the
        get_types method."""

    def put_object(params, path=''):
        """
        Put or set the given params on an object of path or context. The params
        keys should map to the values associated with it from the get_object or
        get_schema methods. """

    def delete_object(path=''):
        """
        Delete the given path or context.
        """

    def get_schema(path='', type=False):
        """
        Delivers a schema in a dictionary format, where keys are attribute names
        and there values are a dictionary of required, type and value information.
        e.g.:
        
        {'attribute_name':
            {'required': (True or False) or (1 or 0)
             'type': lines, text, boolean, etc.
             'value': ... }, ... }
        
        If type is 'True', then no object exists to get a schema from. path in
        this case is the type_name. This indicates two functionalities in one method.
        """


class ITypes(Interface):

    def get_types(path=''):
        """
        get_types returns a list of addable types for a given context.
        """


class IWorkflow(Interface):

    def get_workflow(path=''):
        """
        get_workflow returns the workflow state of the object.
        """

    def set_workflow(transition, path=''):
        """
        set_workflow sets the workflow state of an object.
        """


class IDiscussion(Interface):

    def get_discussion(path=''):
        """
        get_discussion return the DiscussionItemContainer for the object^
        """


class IQuery(Interface):
    """The query interface view for the 'query' API call."""

    def query(filtr={}):
        """search for an object"""

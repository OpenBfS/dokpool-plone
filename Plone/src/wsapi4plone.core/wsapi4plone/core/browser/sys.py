from zope.interface import implements

from interfaces import ISystemAPI

class SystemAPI(object):
    implements(ISystemAPI)

    spec_id = "introspect"
    spec_version = 1
    spec_url = "http://xmlrpc-c.sourceforge.net/introspection.html"

    def get_capabilities(self):
        return {'specId': self.spec_id,
                   'specVersion': self.spec_version,
                   'specUrl': self.spec_url}

    def method_signature(self, method_name):
        pass

    def list_methods(self):
        pass

    def method_help(self, method_name):
        pass

    def multicall(self):
        pass
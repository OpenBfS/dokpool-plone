from zope.interface import implements

from interfaces import ITypes
from wsapi import WSAPI

class Types(WSAPI):
    implements(ITypes)

    def get_types(self, path=''):
        """
        @param path - string to the path of the wanted object
        =returns - a list of tupled types with id and title values (e.g.
            [('Document', 'Page'), ('Link', 'Link'), ... ] ).
        """
        obj = self.builder(self.context, path)
        types = [ (type_.id, type_.title_or_id(),) for type_ in obj.allowedContentTypes() ]
        self.logger.info("- get_types - Getting type names.")
        return types
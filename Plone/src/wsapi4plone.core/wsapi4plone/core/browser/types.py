from wsapi4plone.core.browser.interfaces import ITypes
from wsapi4plone.core.browser.wsapi import WSAPI
from zope.interface import implementer


@implementer(ITypes)
class Types(WSAPI):

    def get_types(self, path=''):
        """
        @param path - string to the path of the wanted object
        =returns - a list of tupled types with id and title values (e.g.
            [('Document', 'Page'), ('Link', 'Link'), ... ] ).
        """
        obj = self.builder(self.context, path)
        types = [(type_.id, type_.title_or_id())
                 for type_ in obj.allowedContentTypes()]
        self.logger.info("- get_types - Getting type names.")
        return types

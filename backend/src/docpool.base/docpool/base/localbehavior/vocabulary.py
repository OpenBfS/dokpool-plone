from docpool.base import DocpoolMessageFactory as _
from docpool.base.appregistry import extendingApps
from zope.component import getMultiAdapter
from zope.globalrequest import getRequest
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def LocalBehaviorsVocabularyFactory(context):
    """Vocabulary factory for available local behaviors based on context.
    
    This factory provides the vocabulary of available applications that can be
    assigned as local behaviors to content objects. The available options depend
    on the context:
    
    - **For doctypes in config**: All behaviors allowed in the DocumentPool are relevant
      - Global config: Applications permitted for the current user
      - Local config: Applications supported in the current DocumentPool
    - **For documents**: Applications must be permitted in the DocumentPool,
      available to the current user, and supported by the document's doctype
    
    The vocabulary excludes applications marked as 'implicit' since these
    are automatically applied and shouldn't be manually selectable.
    
    Args:
        context: The content object context for which to build the vocabulary
        
    Returns:
        SimpleVocabulary: Vocabulary containing available application choices
    """
    request = getRequest()
    path = request.physicalPathFromURL(request.getURL())
    dp_app_state = getMultiAdapter((context, request), name="dp_app_state")
    
    if "config" in path:
        # We're in a configuration context (doctype or DocumentPool config)
        if path.index("config") == 2:  # global config at site level
            apps = dp_app_state.appsPermittedForCurrentUser()
        else:  # local DocumentPool config
            apps = dp_app_state.appsSupportedHere()
        return SimpleVocabulary([
            SimpleTerm(app[0], title=_(app[1]))
            for app in extendingApps()
            if app[0] in apps
            if not app[2]["implicit"]
        ])
    else:
        # We're working with a document - check permitted apps for this object
        available_apps = dp_app_state.appsPermittedForObject(request)
        return SimpleVocabulary([
            SimpleTerm(app[0], title=_(app[1]))
            for app in extendingApps()
            if app[0] in available_apps
            if not app[2]["implicit"]
        ])

from zope.interface import directlyProvides
from zope.component import getUtilitiesFor
from zope.globalrequest import getRequest
from zope.component import getMultiAdapter

from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.behavior.interfaces import IBehavior

from docpool.base.appregistry import extendingApps
from docpool.base.interfaces import IDocumentExtension, IDocTypeExtension
from docpool.base import DocpoolMessageFactory as _

def LocalBehaviorsVocabularyFactory(context):
    """
    The local behaviors available to an object are determined as follows:
    - For a doctype, all behaviors allowed in the docpool are relevant.
    - For a document, the behavior must be allowed in the docpool, available to the current user and supported by the
    doctype of the document.
    @param context:
    @return:
    """
    request = getRequest()
    path = request.physicalPathFromURL(request.getURL())
    isType = False
    dp_app_state = getMultiAdapter((context, request), name=u'dp_app_state')
    if 'config' in path:
        isType = True
        apps = dp_app_state.appsSupportedHere()
        return SimpleVocabulary([SimpleTerm(app[0], title=_(app[1])) for app in extendingApps() if app[0] in apps])
    else: # It's a document
        available_apps = dp_app_state.appsPermittedForObject(request)
        return SimpleVocabulary([SimpleTerm(app[0], title=_(app[1])) for app in extendingApps() if app[0] in available_apps])

directlyProvides(LocalBehaviorsVocabularyFactory, IVocabularyFactory)

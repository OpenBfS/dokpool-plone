from zope.interface import directlyProvides
from zope.component import getUtilitiesFor
from zope.globalrequest import getRequest

from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from plone.behavior.interfaces import IBehavior
from docpool.base.interfaces import IDocumentExtension, IDocTypeExtension

def LocalBehaviorsVocabularyFactory(context):
    req = getRequest()
    path = req.physicalPathFromURL(req.getURL())
    isType = False
    if 'config' in path:
        isType = True
    behaviors = getUtilitiesFor(IBehavior)
    if isType:
        items = [
            (reg.interface.__identifier__, reg.title) for (
                title, reg) in behaviors if (
                reg.interface.extends(IDocTypeExtension)
            )
            ]
    else:
        items = [
            (reg.interface.__identifier__, reg.title) for (
                title, reg) in behaviors if (
                reg.interface.extends(IDocumentExtension)
            )
            ]
    return SimpleVocabulary.fromItems(items)

directlyProvides(LocalBehaviorsVocabularyFactory, IVocabularyFactory)

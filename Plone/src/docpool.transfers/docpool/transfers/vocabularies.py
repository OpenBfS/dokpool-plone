from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory, IBaseVocabulary
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from docpool.transfers import DocpoolMessageFactory as _
from AccessControl.SecurityInfo import allow_module, allow_class
from Products.Archetypes.utils import shasattr
from docpool.base.utils import getDocumentPoolSite
from docpool.base.utils import getAllowedDocumentTypesForGroup


class PermissionsVocabulary(object):
    """
    """
    implements(IVocabularyFactory)
    
    def __call__(self, context):
        return SimpleVocabulary([SimpleTerm('write', title=_('write')),SimpleTerm('read/write', title=_('read/write')),SimpleTerm('suspend', title=_('suspended'))])
    
PermissionsVocabularyFactory = PermissionsVocabulary()

class UnknownOptionsVocabulary(object):
    """
    """
    implements(IVocabularyFactory)
    
    def __call__(self, context):
        return SimpleVocabulary([SimpleTerm('block', title=_('don\'t accept')),SimpleTerm('confirm', title=_('needs confirmation'))])
    
UnknownOptionsVocabularyFactory = UnknownOptionsVocabulary()

class DTPermOptionsVocabulary(object):
    """
    """
    implements(IVocabularyFactory)
    
    def __call__(self, context):
        return SimpleVocabulary([SimpleTerm('block', title=_('don\'t accept')),SimpleTerm('confirm', title=_('needs confirmation')),SimpleTerm('publish', title=_('publish immediately'))])
    
DTPermOptionsVocabularyFactory = DTPermOptionsVocabulary()


allow_module("docpool.transfers.vocabularies")

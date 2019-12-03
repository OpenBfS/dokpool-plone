# -*- coding: utf-8 -*-
from docpool.doksys import _
from Products.CMFPlone.utils import safe_encode
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class LegalBase(object):

    def __call__(self, context=None):
        items = [
            (u'AVV IMIS', _(u'AVV IMIS')),
            (u'EURDEP', _(u'EURDEP')),
            (u'IRMIS', _(u'IRMIS')),
            (u'DENSE', _(u'DENSE')),
            (u'KFÜ', _(u'KFÜ')),
            (u'Land', _(u'Land')),
            (u'SPARSE', _(u'SPARSE')),
            (u'REI-E', _(u'REI-E')),
            (u'REI-I', _(u'REI-I')),
        ]
        terms = [SimpleTerm(value, safe_encode(value), title)
                 for value, title in items]
        return SimpleVocabulary(terms)


LegalBaseFactory = LegalBase()

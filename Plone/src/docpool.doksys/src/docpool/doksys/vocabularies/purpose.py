# -*- coding: utf-8 -*-
from docpool.doksys import _
from Products.CMFPlone.utils import safe_encode
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class Purpose(object):

    def __call__(self, context=None):
        items = [
            (u'Standard-Info Bundesmessnetze', _(u'Standard-Info Bundesmessnetze')),
            (u'Standard-Info DWD', _(u'Standard-Info DWD')),
        ]

        terms = [SimpleTerm(value, safe_encode(value), title)
                 for value, title in items]
        return SimpleVocabulary(terms)


PurposeFactory = Purpose()

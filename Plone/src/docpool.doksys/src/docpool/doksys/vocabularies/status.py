# -*- coding: utf-8 -*-
from docpool.doksys import _
from Products.CMFPlone.utils import safe_encode
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class Status(object):
    """
    """

    def __call__(self, context=None):
        items = [
            (u'geprueft', _(u'geprueft')),
            (u'nicht geprueft', _(u'nicht geprueft')),
        ]
        terms = [SimpleTerm(value, value, title)
                 for value, title in items]
        return SimpleVocabulary(terms)


StatusFactory = Status()

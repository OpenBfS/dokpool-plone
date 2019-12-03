# -*- coding: utf-8 -*-
from docpool.doksys import _
from Products.CMFPlone.utils import safe_encode
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class Duration(object):

    def __call__(self, context=None):
        items = [
            (u'1a', _(u'1a')),
            (u'1Mo', _(u'1Mo')),
            (u'1d', _(u'1d')),
            (u'2h', _(u'2h')),
            (u'1h', _(u'1h')),
            (u'10Min', _(u'10Min')),
        ]
        terms = [SimpleTerm(value, safe_encode(value), title)
                 for value, title in items]
        return SimpleVocabulary(terms)


DurationFactory = Duration()

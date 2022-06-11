# -*- coding: utf-8 -*-
from docpool.doksys import _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class OperationMode(object):
    """
    """

    def __call__(self, context=None):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = [
            (u'Routine', _(u'Routine')),
            (u'Intensiv', _(u'Intensiv')),
        ]
        terms = [SimpleTerm(value, value, title)
                 for value, title in items]
        return SimpleVocabulary(terms)


OperationModeFactory = OperationMode()

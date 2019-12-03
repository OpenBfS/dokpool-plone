# -*- coding: utf-8 -*-
from docpool.doksys import _
from Products.CMFPlone.utils import safe_encode
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class MeasuringProgram(object):

    def __call__(self, context=None):
        items = [
            (u'Intensivmessprogramm', _(u'Intensivmessprogramm')),
            (u'Routinemessprogramm', _(u'Routinemessprogramm')),
            (u'REI', _(u'REI')),
            (u'Spontanproben Bund', _(u'Spontanproben Bund')),
        ]
        terms = [SimpleTerm(value, safe_encode(value), title)
                 for value, title in items]
        return SimpleVocabulary(terms)


MeasuringProgramFactory = MeasuringProgram()

# -*- coding: utf-8 -*-
from docpool.doksys import _
from Products.CMFPlone.utils import safe_encode
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class InfoType(object):

    def __call__(self, context=None):
        items = [
            (u'vorwaerts', _(u'vorwaerts')),
            (u'rueckwaerts', _(u'rueckwaerts')),
            (u'brutto', _(u'brutto')),
            (u'netto', _(u'netto')),
            (u'nass', _(u'nass')),
            (u'trocken', _(u'trocken')),
            (u'Messergebnisse', _(u'Messergebnisse')),
            (u'Ueberblick', _(u'Ueberblick')),
            (u'Soll-Ist-Vergleich', _(u'Soll-Ist-Vergleich')),
        ]
        terms = [SimpleTerm(value, safe_encode(value), title)
                 for value, title in items]
        return SimpleVocabulary(terms)


InfoTypeFactory = InfoType()

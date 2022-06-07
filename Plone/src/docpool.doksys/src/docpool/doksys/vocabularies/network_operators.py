# -*- coding: utf-8 -*-
from docpool.doksys import _
from Products.CMFPlone.utils import safe_encode
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class NetworkOperators(object):

    def __call__(self, context=None):
        items = [
            (u'Schleswig-Holstein', _(u'Schleswig-Holstein')),
            (u'Hamburg', _(u'Hamburg')),
            (u'Niedersachsen', _(u'Niedersachsen')),
            (u'Bremen', _(u'Bremen')),
            (u'Nordrhein-Westfalen', _(u'Nordrhein-Westfalen')),
            (u'Hessen', _(u'Hessen')),
            (u'Rheinland-Pfalz', _(u'Rheinland-Pfalz')),
            (u'Baden-Wuerttemberg', _(u'Baden-Wuerttemberg')),
            (u'Bayern', _(u'Bayern')),
            (u'Saarland', _(u'Saarland')),
            (u'Berlin', _(u'Berlin')),
            (u'Brandenburg', _(u'Brandenburg')),
            (u'Mecklenburg-Vorpommern', _(u'Mecklenburg-Vorpommern')),
            (u'Sachsen', _(u'Sachsen')),
            (u'Sachsen-Anhalt', _(u'Sachsen-Anhalt')),
            (u'Thueringen', _(u'Thueringen')),
            (u'Bundeswehr', _(u'Bundeswehr')),
            (u'Endlager (Bundesaufsicht)', _(u'Endlager (Bundesaufsicht)')),
            (u'ZdB-Testnetz', _(u'ZdB-Testnetz')),
            (u'BfS (Spuren)', _(u'BfS (Spuren)')),
            (u'vTI', _(u'vTI')),
            (u'BfS/ZdB', _(u'BfS/ZdB')),
            (u'BfE', _(u'BfE')),
            (u'FhG', _(u'FhG')),
            (u'BfG', _(u'BfG')),
            (u'BSH', _(u'BSH')),
            (u'BfS (LSt. AB)', _(u'BfS (LSt. AB)')),
            (u'BfS (LSt. TW ...)', _(u'BfS (LSt. TW ...)')),
            (u'BMU', _(u'BMU')),
            (u'MRI', _(u'MRI')),
            (u'Park', _(u'Park')),
            (u'Sonstige', _(u'Sonstige')),
            (u'PTB', _(u'PTB')),
            (u'BfS (ABI)', _(u'BfS (ABI)')),
            (u'DWD', _(u'DWD')),
            (u'auslaend. Messnetze', _(u'auslaend. Messnetze')),
            (u'BfS (ODL)', _(u'BfS (ODL)')),
        ]
        terms = [SimpleTerm(value, value, title)
                 for value, title in items]
        return SimpleVocabulary(terms)


NetworkOperatorsFactory = NetworkOperators()

# -*- coding: utf-8 -*-

# from plone import api
from docpool.doksys import _
from plone.dexterity.interfaces import IDexterityContent
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class VocabItem(object):
    def __init__(self, token, value):
        self.token = token
        self.value = value


@implementer(IVocabularyFactory)
class NetworkOperators(object):
    """
    """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = [
            VocabItem(u'Schleswig-Holstein', _(u'Schleswig-Holstein')),
            VocabItem(u'Hamburg', _(u'Hamburg')),
            VocabItem(u'Niedersachsen', _(u'Niedersachsen')),
            VocabItem(u'Bremen', _(u'Bremen')),
            VocabItem(u'Nordrhein-Westfalen', _(u'Nordrhein-Westfalen')),
            VocabItem(u'Hessen', _(u'Hessen')),
            VocabItem(u'Rheinland-Pfalz', _(u'Rheinland-Pfalz')),
            VocabItem(u'Baden-Wuerttemberg', _(u'Baden-Wuerttemberg')),
            VocabItem(u'Bayern', _(u'Bayern')),
            VocabItem(u'Saarland', _(u'Saarland')),
            VocabItem(u'Berlin', _(u'Berlin')),
            VocabItem(u'Brandenburg', _(u'Brandenburg')),
            VocabItem(u'Mecklenburg-Vorpommern', _(u'Mecklenburg-Vorpommern')),
            VocabItem(u'Sachsen', _(u'Sachsen')),
            VocabItem(u'Sachsen-Anhalt', _(u'Sachsen-Anhalt')),
            VocabItem(u'Thueringen', _(u'Thueringen')),
            VocabItem(u'Bundeswehr', _(u'Bundeswehr')),
            VocabItem(u'Endlager (Bundesaufsicht)', _(u'Endlager (Bundesaufsicht)')),
            VocabItem(u'ZdB-Testnetz', _(u'ZdB-Testnetz')),
            VocabItem(u'BfS (Spuren)', _(u'BfS (Spuren)')),
            VocabItem(u'vTI', _(u'vTI')),
            VocabItem(u'BfS/ZdB', _(u'BfS/ZdB')),
            VocabItem(u'BfE', _(u'BfE')),
            VocabItem(u'FhG', _(u'FhG')),
            VocabItem(u'BfG', _(u'BfG')),
            VocabItem(u'BSH', _(u'BSH')),
            VocabItem(u'BfS (LSt. AB)', _(u'BfS (LSt. AB)')),
            VocabItem(u'BfS (LSt. TW ...)', _(u'BfS (LSt. TW ...)')),
            VocabItem(u'BMU', _(u'BMU')),
            VocabItem(u'MRI', _(u'MRI')),
            VocabItem(u'Park', _(u'Park')),
            VocabItem(u'Sonstige', _(u'Sonstige')),
            VocabItem(u'PTB', _(u'PTB')),
            VocabItem(u'BfS (ABI)', _(u'BfS (ABI)')),
            VocabItem(u'DWD', _(u'DWD')),
            VocabItem(u'auslaend. Messnetze', _(u'auslaend. Messnetze')),
            VocabItem(u'BfS (ODL)', _(u'BfS (ODL)')),
        ]

        # Fix context if you are using the vocabulary in DataGridField.
        # See https://github.com/collective/collective.z3cform.datagridfield/issues/31:  # NOQA: 501
        if not IDexterityContent.providedBy(context):
            req = getRequest()
            context = req.PARENTS[0]

        # create a list of SimpleTerm items:
        terms = []
        for item in items:
            terms.append(
                SimpleTerm(
                    value=item.token, token=item.token.encode('utf'), title=item.value
                )
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


NetworkOperatorsFactory = NetworkOperators()

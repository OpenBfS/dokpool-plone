# -*- coding: utf-8 -*-
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory


@implementer(IVocabularyFactory)
class DataType(object):

    def __call__(self, context=None):
        values = [
            u'ONMON',
            u'LADA',
            u'EURDEP',
        ]
        return safe_simplevocabulary_from_values(values)


DataTypeFactory = DataType()

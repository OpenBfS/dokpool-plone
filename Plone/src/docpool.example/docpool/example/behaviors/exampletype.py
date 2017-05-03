# -*- coding: utf-8 -*-
#
# File: exampletype.py
#
# Copyright (c) 2017 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""
"""
from zope import schema
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import provider, implementer
from plone.directives import form

##code-section imports
from Acquisition import aq_inner
from docpool.base.interfaces import IDocTypeExtension
##/code-section imports


from docpool.example import DocpoolMessageFactory as _

@provider(IFormFieldProvider)
class IExampleType(IDocTypeExtension):
    example_type_attribute = schema.TextLine(
                        title=_(u'label_example_type_attribute', default=u'Example Type Attribute'),
                        description=_(u'description_example_type_attribute', default=u''),
                        required=False,
    )


##/code-section interface


class ExampleType(object):
    """
    """

    def __init__(self, context):
        self.context = context
##code-section methods

    def _get_example_type_attribute(self):
        return self.context.example_type_attribute

    def _set_example_type_attribute(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.example_type_attribute = value

    example_type_attribute = property(_get_example_type_attribute, _set_example_type_attribute)

##/code-section methods


##code-section bottom
##/code-section bottom 
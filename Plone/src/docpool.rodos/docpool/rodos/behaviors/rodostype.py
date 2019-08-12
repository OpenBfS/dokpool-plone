# -*- coding: utf-8 -*-
#
# File: rodostype.py
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

from Acquisition import aq_inner
from docpool.base.interfaces import IDocTypeExtension


from docpool.rodos import DocpoolMessageFactory as _

@provider(IFormFieldProvider)
class IRodosType(IDocTypeExtension):
    pass



class RodosType(object):
    """
    """

    def __init__(self, context):
        self.context = context



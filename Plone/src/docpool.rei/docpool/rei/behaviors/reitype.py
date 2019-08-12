# -*- coding: utf-8 -*-
#
# File: reitype.py
#
# Copyright (c) 2017 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""
"""
from docpool.base.interfaces import IDocTypeExtension
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import provider


@provider(IFormFieldProvider)
class IREIType(IDocTypeExtension):
    pass


class REIType(object):
    """
    """

    def __init__(self, context):
        self.context = context

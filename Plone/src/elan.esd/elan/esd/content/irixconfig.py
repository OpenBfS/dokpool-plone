# -*- coding: utf-8 -*-
#
# File: irixconfig.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the IRIXConfig content type. See irixconfig.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from elan.esd import DocpoolMessageFactory as _
from plone.dexterity.content import Item
from plone.directives import form
from zope import schema
from zope.interface import implements


class IIRIXConfig(form.Schema):
    """
    """

    organisationReporting = schema.TextLine(
        title=_(
            u'label_irixconfig_organisationreporting',
            default=u'Reporting State / Organisation',
        ),
        description=_(u'description_irixconfig_organisationreporting', default=u''),
        required=True,
    )

    contactName = schema.TextLine(
        title=_(u'label_irixconfig_contactname', default=u'Name of contact'),
        description=_(u'description_irixconfig_contactname', default=u''),
        required=True,
    )

    contactEmail = schema.TextLine(
        title=_(u'label_irixconfig_contactemail', default=u'Email of contact'),
        description=_(u'description_irixconfig_contactemail', default=u''),
        required=True,
    )

    organisationName = schema.TextLine(
        title=_(u'label_irixconfig_organisationname', default=u'Name of organisation'),
        description=_(u'description_irixconfig_organisationname', default=u''),
        required=True,
    )

    organisationId = schema.TextLine(
        title=_(u'label_irixconfig_organisationid', default=u'ID of organisation'),
        description=_(u'description_irixconfig_organisationid', default=u''),
        required=True,
    )

    organisationCountry = schema.TextLine(
        title=_(u'label_irixconfig_organisationcountry', default=u'Country code'),
        description=_(u'description_irixconfig_organisationcountry', default=u''),
        required=True,
    )

    organisationWeb = schema.TextLine(
        title=_(u'label_irixconfig_organisationweb', default=u'Web address'),
        description=_(u'description_irixconfig_organisationweb', default=u''),
        required=True,
    )

    organisationEmail = schema.TextLine(
        title=_(u'label_irixconfig_organisationemail', default=u'Email address'),
        description=_(u'description_irixconfig_organisationemail', default=u''),
        required=True,
    )

    sourceText = schema.TextLine(
        title=_(u'label_irixconfig_sourcetext', default=u'Information source text'),
        description=_(u'description_irixconfig_sourcetext', default=u''),
        required=True,
    )

    sourceDescription = schema.TextLine(
        title=_(
            u'label_irixconfig_sourcedescription',
            default=u'Information source description',
        ),
        description=_(u'description_irixconfig_sourcedescription', default=u''),
        required=True,
    )

    typeMapping = schema.Text(
        title=_(
            u'label_irixconfig_typemapping', default=u' ELAN types 2 IRIX type mapping'
        ),
        description=_(u'description_irixconfig_typemapping', default=u''),
        required=True,
    )


class IRIXConfig(Item):
    """
    """

    security = ClassSecurityInfo()

    implements(IIRIXConfig)

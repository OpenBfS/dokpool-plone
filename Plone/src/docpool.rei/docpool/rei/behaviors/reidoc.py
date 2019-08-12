# -*- coding: utf-8 -*-
"""Common configuration constants
"""
from Products.Archetypes.utils import shasattr
from docpool.base.utils import getInheritedValue

from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform.directives import read_permission, write_permission
from plone.autoform import directives as form
from z3c.form.browser.checkbox import CheckBoxFieldWidget

# from plone.directives import form
from zope.interface import provider, implementer
from zope import schema
from docpool.base import DocpoolMessageFactory as _
from docpool.base.browser.flexible_view import FlexibleView
from docpool.rei.config import REI_APP
from AccessControl import ClassSecurityInfo
from docpool.base.interfaces import IDocumentExtension
from collective import dexteritytextindexer
from Products.CMFPlone.utils import parent

from z3c.form.browser.radio import RadioFieldWidget

from docpool.rei import DocpoolMessageFactory as _

from Acquisition import aq_inner
from plone.formwidget.autocomplete import AutocompleteFieldWidget


@provider(IFormFieldProvider)
class IREIDoc(IDocumentExtension):

    Authority = schema.Choice(
        title=_(u'label_rei_Authority', default=u'Authority'),
        description=_(u'description_rei_Authority', default=u''),
        source="docpool.rei.vocabularies.AuthorityVocabulary",
        required=True,
    )
    read_permission(Authority='docpool.rei.AccessRei')
    write_permission(Authority='docpool.rei.AccessRei')
    dexteritytextindexer.searchable('Authority')

    MstId = schema.List(
        title=_(u'label_rei_MstId', default=u'Messstellen-ID'),
        description=_(u'description_rei_MstId', default=u''),
        value_type=schema.Choice(source="docpool.rei.vocabularies.MstVocabulary"),
        required=False,
    )
    read_permission(MstId='docpool.rei.AccessRei')
    write_permission(MstId='docpool.rei.AccessRei')
    dexteritytextindexer.searchable('Messstelle')

    ReiLegalBase = schema.Choice(
        title=_(u'label_rei_ReiLegalBase', default=u'ReiLegalBase'),
        description=_(u'description_rei_ReiLegalBase', default=u''),
        source="docpool.rei.vocabularies.ReiLegalBaseVocabulary",
        required=True,
    )
    read_permission(ReiLegalBase='docpool.rei.AccessRei')
    write_permission(ReiLegalBase='docpool.rei.AccessRei')
    dexteritytextindexer.searchable('ReiLegalBase')

    form.widget(Origin=CheckBoxFieldWidget)
    Origin = schema.List(
        title=_(u'label_rei_Origin', default=u'Ersteller'),
        description=_(u'description_rei_Origin', default=u''),
        value_type=schema.Choice(source=u"docpool.rei.vocabularies.OriginVocabulary"),
        required=True,
    )
    read_permission(Origin='docpool.rei.AccessRei')
    write_permission(Origin='docpool.rei.AccessRei')
    dexteritytextindexer.searchable('Origin')

    Year = schema.Choice(
        title=_(u'label_rei_Year', default=u'Year'),
        description=_(u'description_rei_Year', default=u''),
        source="docpool.rei.vocabularies.YearVocabulary",
        required=True,
    )
    read_permission(Year='docpool.rei.AccessRei')
    write_permission(Year='docpool.rei.AccessRei')
    dexteritytextindexer.searchable('Year')

    Period = schema.Choice(
        title=_(u'label_rei_Period', default=u'Period'),
        description=_(u'description_rei_Period', default=u''),
        source="docpool.rei.vocabularies.PeriodVocabulary",
        required=True,
    )
    read_permission(Period='docpool.rei.AccessRei')
    write_permission(Period='docpool.rei.AccessRei')
    dexteritytextindexer.searchable('Period')

    Media = schema.Choice(
        title=_(u'label_rei_Media', default=u'Media'),
        description=_(u'description_rei_Media', default=u''),
        source="docpool.rei.vocabularies.MediaVocabulary",
        required=False,
    )
    read_permission(Media='docpool.rei.AccessRei')
    write_permission(Media='docpool.rei.AccessRei')
    dexteritytextindexer.searchable('Media')

    NuclearInstallation = schema.Choice(
        title=_(u'label_rei_NuclearInstallation', default=u'NuclearInstallation'),
        description=_(u'description_rei_NuclearInstallation', default=u''),
        source="docpool.rei.vocabularies.NuclearInstallationVocabulary",
        required=True,
    )
    read_permission(NuclearInstallation='docpool.rei.AccessRei')
    write_permission(NuclearInstallation='docpool.rei.AccessRei')
    dexteritytextindexer.searchable('NuclearInstallation')

    StartSampling = schema.Datetime(
        title=_(u'label_rei_StartSampling', default=u'Start Sampling'),
        description=_(u'description_rei_StartSampling', default=u''),
        required=True,
    )
    read_permission(StartSampling='docpool.rei.AccessRei')
    write_permission(StartSampling='docpool.rei.AccessRei')

    StopSampling = schema.Datetime(
        title=_(u'label_rei_StopSampling', default=u'Stop Sampling'),
        description=_(u'description_rei_StopSampling', default=u''),
        required=True,
    )
    read_permission(StopSampling='docpool.rei.AccessRei')
    write_permission(StopSampling='docpool.rei.AccessRei')

    PdfVersion = schema.Choice(
        title=_(u'label_rei_PdfVersion', default=u'Pdf Version'),
        description=_(u'description_rei_PdfVersion', default=u''),
        source="docpool.rei.vocabularies.PdfVersionVocabulary",
        required=True,
    )
    read_permission(PdfVersion='docpool.rei.AccessRei')
    write_permission(PdfVersion='docpool.rei.AccessRei')
    dexteritytextindexer.searchable('PdfVersion')


class REIDoc(FlexibleView):
    __allow_access_to_unprotected_subobjects__ = 1

    security = ClassSecurityInfo()

    appname = REI_APP

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST

    def _get_rei_StartSampling(self):
        return getInheritedValue(self, "StartSampling")

    def _set_rei_StartSampling(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.StartSampling = value

    StartSampling = property(_get_rei_StartSampling, _set_rei_StartSampling)

    def _get_rei_StopSampling(self):
        return getInheritedValue(self, "StopSampling")

    def _set_rei_StopSampling(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.StopSampling = value

    StopSampling = property(_get_rei_StopSampling, _set_rei_StopSampling)

    def _get_rei_FederalState(self):
        return getInheritedValue(self, "FederalState")

    def _set_rei_FederalState(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.FederalState = value

    FederalState = property(_get_rei_FederalState, _set_rei_FederalState)

    def _get_rei_Operator(self):
        return getInheritedValue(self, "Operator")

    def _set_rei_Operator(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.Operator = value

    Operator = property(_get_rei_Operator, _set_rei_Operator)

    def _get_rei_MstId(self):
        return getInheritedValue(self, "Messstellen-ID")

    def _set_rei_MstId(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.MstId = value

    MstId = property(_get_rei_MstId, _set_rei_MstId)

    def _get_rei_ReiLegalBase(self):
        return getInheritedValue(self, "ReiLegalBase")

    def _set_rei_ReiLegalBase(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.ReiLegalBase = value

    ReiLegalBase = property(_get_rei_ReiLegalBase, _set_rei_ReiLegalBase)

    def _get_rei_Year(self):
        return getInheritedValue(self, "Year")

    def _set_rei_Year(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.Year = value

    Year = property(_get_rei_Year, _set_rei_Year)

    def _get_rei_Period(self):
        return getInheritedValue(self, "Period")

    def _set_rei_Period(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.Period = value

    Period = property(_get_rei_Period, _set_rei_Period)

    def _get_rei_Media(self):
        return getInheritedValue(self, "Media")

    def _set_rei_Media(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.Media = value

    Media = property(_get_rei_Media, _set_rei_Media)

    def _get_rei_NuclearInstallation(self):
        return getInheritedValue(self, "NuclearInstallation")

    def _set_rei_NuclearInstallation(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.NuclearInstallation = value

    NuclearInstallation = property(
        _get_rei_NuclearInstallation, _set_rei_NuclearInstallation
    )

    def _get_rei_PdfVersion(self):
        return getInheritedValue(self, "PdfVersion")

    def _set_rei_PdfVersion(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.PdfVersion = value

    PdfVersion = property(_get_rei_PdfVersion, _set_rei_PdfVersion)

    def _get_rei_Origin(self):
        return getInheritedValue(self, "Origin")

    def _set_rei_Origin(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.Origin = value

    Origin = property(_get_rei_Origin, _set_rei_Origin)

    def isClean(self):
        """
        Is this document free for further action like publishing or transfer?
        @return:
        """
        # TODO: define if necessary. Method MUST be present in Doc behavior.
        return True

# -*- coding: utf-8 -*-
"""Common configuration constants
"""
from AccessControl import ClassSecurityInfo
from collective import dexteritytextindexer
from datetime import date
from docpool.base.browser.flexible_view import FlexibleView
from docpool.base.interfaces import IDocumentExtension
from docpool.rei import DocpoolMessageFactory as _
from docpool.rei.config import REI_APP
from plone import api
from plone.autoform import directives
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.autoform.interfaces import IFormFieldProvider
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import provider


START_SAMPLING_MAPPING = {
    'Q1': '1.1.',
    'Q2': '1.4.',
    'Q3': '1.7.',
    'Q4': '1.10.',
    'H1': '1.1.',
    'H2': '1.7.',
    'Y': '1.1.',
    'M1': '1.1.',
    'M2': '1.2.',
    'M3': '1.3.',
    'M4': '1.4.',
    'M5': '1.5.',
    'M6': '1.6.',
    'M7': '1.7.',
    'M8': '1.8.',
    'M9': '1.9.',
    'M10': '1.10.',
    'M11': '1.11.',
    'M12': '1.12.',
}

STOP_SAMPLING_MAPPING = {
    'Q1': '1.4.',
    'Q2': '1.7.',
    'Q3': '1.10.',
    'Q4': '1.1.',
    'H1': '1.7.',
    'H2': '1.1.',
    'Y': '1.1.',
    'M1': '1.2.',
    'M2': '1.3.',
    'M3': '1.4.',
    'M4': '1.5.',
    'M5': '1.6.',
    'M6': '1.7.',
    'M7': '1.8.',
    'M8': '1.9.',
    'M9': '1.10.',
    'M10': '1.11.',
    'M11': '1.12.',
    'M12': '1.1.',
}


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

    MstIds = schema.List(
        title=_(u'label_rei_MstId', default=u'Messstellen-ID'),
        description=_(u'description_rei_MstId', default=u''),
        value_type=schema.Choice(
            source="docpool.rei.vocabularies.MstVocabulary"),
        required=False,
    )
    read_permission(MstIds='docpool.rei.AccessRei')
    write_permission(MstIds='docpool.rei.AccessRei')

    directives.widget(ReiLegalBases=CheckBoxFieldWidget)
    ReiLegalBases = schema.List(
        title=_(u'label_rei_ReiLegalBases', default=u'ReiLegalBases'),
        description=_(u'description_rei_ReiLegalBases', default=u''),
        value_type=schema.Choice(
            source=u"docpool.rei.vocabularies.ReiLegalBaseVocabulary"),
        required=True,
    )
    read_permission(ReiLegalBases='docpool.rei.AccessRei')
    write_permission(ReiLegalBases='docpool.rei.AccessRei')
    dexteritytextindexer.searchable('ReiLegalBases')

    directives.widget(Origin=CheckBoxFieldWidget)
    Origin = schema.List(
        title=_(u'label_rei_Origin', default=u'Ersteller'),
        description=_(u'description_rei_Origin', default=u''),
        value_type=schema.Choice(
            source=u"docpool.rei.vocabularies.OriginVocabulary"),
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

    Medium = schema.Choice(
        title=_(u'label_rei_Medium', default=u'Medium'),
        description=_(u'description_rei_Medium', default=u''),
        source="docpool.rei.vocabularies.MediaVocabulary",
        required=False,
    )
    read_permission(Medium='docpool.rei.AccessRei')
    write_permission(Medium='docpool.rei.AccessRei')
    dexteritytextindexer.searchable('Medium')

    NuclearInstallations = schema.List(
        title=_(
            u'label_rei_NuclearInstallation',
            default=u'NuclearInstallations'),
        description=_(u'description_rei_NuclearInstallation', default=u''),
        value_type=schema.Choice(
        source="docpool.rei.vocabularies.NuclearInstallationVocabulary"),
        required=True,
    )
    read_permission(NuclearInstallations='docpool.rei.AccessRei')
    write_permission(NuclearInstallations='docpool.rei.AccessRei')
    dexteritytextindexer.searchable('NuclearInstallations')

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

    @property
    def Authority(self):
        return self.context.Authority

    @Authority.setter
    def Authority(self, value):
        self.context.Authority = value

    @property
    def MstIds(self):
        return self.context.MstIds

    @MstIds.setter
    def MstIds(self, value):
        self.context.MstIds = value

    @property
    def ReiLegalBases(self):
        return self.context.ReiLegalBases

    @ReiLegalBases.setter
    def ReiLegalBases(self, value):
        self.context.ReiLegalBases = value

    @property
    def Year(self):
        return self.context.Year

    @Year.setter
    def Year(self, value):
        self.context.Year = value

    @property
    def Period(self):
        return self.context.Period

    @Period.setter
    def Period(self, value):
        self.context.Period = value

    @property
    def Medium(self):
        return self.context.Medium

    @Medium.setter
    def Medium(self, value):
        self.context.Medium = value

    @property
    def NuclearInstallations(self):
        return self.context.NuclearInstallations

    @NuclearInstallations.setter
    def NuclearInstallations(self, value):
        self.context.NuclearInstallations = value

    @property
    def PdfVersion(self):
        return self.context.PdfVersion

    @PdfVersion.setter
    def PdfVersion(self, value):
        self.context.PdfVersion = value

    @property
    def Origin(self):
        return self.context.Origin

    @Origin.setter
    def Origin(self, value):
        self.context.Origin = value

    def isClean(self):
        """
        Is this document free for further action like publishing or transfer?
        @return:
        """
        # TODO: define if necessary. Method MUST be present in Doc behavior.
        return True

    @property
    def StartSampling(self):
        date_fragment = START_SAMPLING_MAPPING[self.Period]
        day, month, _ = date_fragment.split('.')
        day, month = int(day), int(month)
        year = int(self.Year)
        return date(year=year, month=month, day=day)

    @property
    def StopSampling(self):
        date_fragment = STOP_SAMPLING_MAPPING[self.Period]
        day, month, _ = date_fragment.split('.')
        day, month = int(day), int(month)
        year = int(self.Year)
        if month == 1:
            year += 1
        return date(year=year, month=month, day=day)

    def sampling_start_localized(self):
        return api.portal.get_localized_time(self.StartSampling)

    def sampling_stop_localized(self):
        return api.portal.get_localized_time(self.StopSampling)

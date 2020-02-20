# -*- coding: utf-8 -*-
"""Common configuration constants
"""
from AccessControl import ClassSecurityInfo
from collective import dexteritytextindexer
from datetime import date
from docpool.base.browser.flexible_view import FlexibleView
from docpool.base.interfaces import IDocumentExtension
from docpool.base.interfaces import IDPDocument
from docpool.rei import DocpoolMessageFactory as _
from docpool.rei.config import REI_APP
from plone import api
from plone.autoform import directives
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.autoform.interfaces import IFormFieldProvider
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.component import adapter
from zope.component import getUtility
from zope.interface import provider
from zope.lifecycleevent import IObjectAddedEvent
from zope.lifecycleevent import IObjectModifiedEvent
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import RequiredMissing


START_SAMPLING_MAPPING = {
    'Y': '1.1.',
    'H1': '1.1.',
    'H2': '1.7.',
    'Q1': '1.1.',
    'Q2': '1.4.',
    'Q3': '1.7.',
    'Q4': '1.10.',
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
    'Y': '1.1.',
    'H1': '1.7.',
    'H2': '1.1.',
    'Q1': '1.4.',
    'Q2': '1.7.',
    'Q3': '1.10.',
    'Q4': '1.1.',
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

def required(value):
    if not value:
        raise RequiredMissing()
    return True


@provider(IFormFieldProvider)
class IREIDoc(IDocumentExtension):

    NuclearInstallations = schema.List(
        title=_(
            u'label_rei_NuclearInstallations',
            default=u'NuclearInstallations'),
        description=_(u'description_rei_NuclearInstallation', default=u''),
        value_type=schema.Choice(
        source="docpool.rei.vocabularies.NuclearInstallationVocabulary"),
        required=True,
        constraint=required,
    )
    read_permission(NuclearInstallations='docpool.rei.AccessRei')
    write_permission(NuclearInstallations='docpool.rei.AccessRei')
    dexteritytextindexer.searchable('NuclearInstallations')

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

    Medium = schema.Choice(
        title=_(u'label_rei_Medium', default=u'Medium'),
        description=_(u'description_rei_Medium', default=u''),
        source="docpool.rei.vocabularies.MediumVocabulary",
        required=False,
    )
    read_permission(Medium='docpool.rei.AccessRei')
    write_permission(Medium='docpool.rei.AccessRei')
    dexteritytextindexer.searchable('Medium')

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

    directives.widget(Origins=CheckBoxFieldWidget)
    Origins = schema.List(
        title=_(u'label_rei_Origin', default=u'Berichtende Stelle'),
        description=_(u'description_rei_Origin', default=u''),
        value_type=schema.Choice(
            source=u"docpool.rei.vocabularies.OriginVocabulary"),
        required=True,
    )
    read_permission(Origins='docpool.rei.AccessRei')
    write_permission(Origins='docpool.rei.AccessRei')
    dexteritytextindexer.searchable('Origins')


    MStIDs = schema.List(
        title=_(u'label_rei_MStID', default=u'Bericht enthält Daten folgender Messstellen'),
        description=_(u'description_rei_MStID', default=u''),
        value_type=schema.Choice(
            source="docpool.rei.vocabularies.MStIDVocabulary"),
        required=False,
    )
    read_permission(MStIDs='docpool.rei.AccessRei')
    write_permission(MStIDs='docpool.rei.AccessRei')

    mstids_initial_value = schema.TextLine(
        title=_(u'label_rei_mstids_initial_value', default=u'Bericht enthält Daten folgender Messstellen'),
        required=False,
    )
    directives.omitted('mstids_initial_value')

    Authority = schema.Choice(
        title=_(u'label_rei_Authority', default=u'Authority'),
        description=_(u'description_rei_Authority', default=u''),
        source="docpool.rei.vocabularies.AuthorityVocabulary",
        required=True,
    )
    read_permission(Authority='docpool.rei.AccessRei')
    write_permission(Authority='docpool.rei.AccessRei')
    dexteritytextindexer.searchable('Authority')

    PDFVersion = schema.Choice(
        title=_(u'label_rei_PDFVersion', default=u'PDF Version'),
        description=_(u'description_rei_PDFVersion', default=u''),
        source="docpool.rei.vocabularies.PDFVersionVocabulary",
        required=True,
        default='keine Angabe',
    )
    directives.omitted('PDFVersion')
    dexteritytextindexer.searchable('PDFVersion')


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
    def MStIDs(self):
        return self.context.MStIDs

    @MStIDs.setter
    def MStIDs(self, value):
        self.context.MStIDs = value

    @property
    def mstids_initial_value(self):
        return self.context.mstids_initial_value

    @mstids_initial_value.setter
    def mstids_initial_value(self, value):
        self.context.mstids_initial_value = value

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
    def PDFVersion(self):
        return self.context.PDFVersion

    @PDFVersion.setter
    def PDFVersion(self, value):
        self.context.PDFVersion = value

    @property
    def Origins(self):
        return self.context.Origins

    @Origins.setter
    def Origins(self, value):
        self.context.Origins = value

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

    def mstids_display(self):
        voc = getUtility(IVocabularyFactory, 'docpool.rei.vocabularies.MStIDVocabulary')()
        return u', '.join(voc.getTerm(i).title for i in self.MStIDs)

    def period_display(self):
        voc = getUtility(IVocabularyFactory, 'docpool.rei.vocabularies.PeriodVocabulary')()
        return u'{} {}'.format(voc.getTerm(self.Period).title, self.Year)


# IREIDoc sets no marker-interface so we cannot constrain
# the suscriber on IREIDoc. Instead we use IDPDocument
@adapter(IDPDocument, IObjectAddedEvent)
def set_title(obj, event=None):
    # Only if it is a IREIDoc.
    try:
        adapted = IREIDoc(obj)
    except Exception:
        return
    legal_base_mapping = {
        u'REI-E': u'Emmissionsbericht',
        u'REI-I': u'Immissionsbericht',
    }
    if len(adapted.ReiLegalBases) > 1:
        legal = u'Immissions- und Emissionsbericht'
    else:
        legal = legal_base_mapping.get(adapted.ReiLegalBases[0])

    period_mapping = {
        u'Y': u'des {}es',
        u'H1': u'des {}es',
        u'H2': u'des {}es',
        u'Q1': u'des {}s',
        u'Q2': u'des {}s',
        u'Q3': u'des {}s',
        u'Q4': u'des {}s',
        u'M1': u'{}',
        u'M2': u'{}',
        u'M3': u'{}',
        u'M4': u'{}',
        u'M5': u'{}',
        u'M6': u'{}',
        u'M7': u'{}',
        u'M8': u'{}',
        u'M9': u'{}',
        u'M10': u'{}',
        u'M11': u'{}',
        u'M12': u'{}',
    }
    period_vocabulary = getUtility(IVocabularyFactory, 'docpool.rei.vocabularies.PeriodVocabulary')()
    period_template = period_mapping.get(adapted.Period)
    period_prefix = period_template.format(period_vocabulary.getTerm(adapted.Period).title)
    period = u'{} {}'.format(period_prefix, adapted.Year)

    installations = adapted.NuclearInstallations
    if len(installations) == 1:
        installations_prefix = u'für die Kerntechnische Anlage'
        installations = installations[0]
    elif len(installations) == 2:
        installations_prefix = u'für die Kerntechnischen Anlagen'
        installations = u' und '.join(installations)
    else:
        installations_prefix = u'für die Kerntechnischen Anlagen'
        part1 = u', '.join(installations[:-1])
        installations = u'{} und {}'.format(part1, installations[-1])

    if adapted.Medium:
        medium = u'({}) '.format(adapted.Medium)
    else:
        medium = u''
    origins = u'({})'.format(', '.join(adapted.Origins))
    new_title = u'REI-{legal} {medium}{period} {installations_prefix} {installations} {origins}'.format(
        legal=legal,
        period=period,
        installations_prefix=installations_prefix,
        installations=installations,
        medium=medium,
        origins=origins,
        )
    obj.title = new_title
    obj.reindexObject(idxs=['Title'])


@adapter(IDPDocument, IObjectAddedEvent)
def save_mstid_added(obj, event=None):
    return save_mstid(obj)


@adapter(IDPDocument, IObjectModifiedEvent)
def save_mstid_modified(obj, event=None):
    return save_mstid(obj)


def save_mstid(obj):
    try:
        adapted = IREIDoc(obj)
    except Exception:
        return
    value = adapted.mstids_display()
    if getattr(adapted, 'mstids_initial_value', None) != value:
        adapted.mstids_initial_value = value

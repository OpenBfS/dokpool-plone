"""Common configuration constants
"""
import re
from datetime import date

from AccessControl import ClassSecurityInfo
from docpool.base.browser.flexible_view import FlexibleView
from docpool.base.interfaces import IDocumentExtension, IDPDocument
from docpool.base.marker import IImportingMarker
from docpool.base.utils import execute_under_special_role
from docpool.rei import DocpoolMessageFactory as _
from docpool.rei.config import REI_APP
from docpool.rei.vocabularies import AuthorityVocabulary
from plone import api
from plone.app.dexterity.textindexer.directives import searchable
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.autoform.directives import read_permission, write_permission
from plone.autoform.interfaces import IFormFieldProvider
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.component import adapter, getUtility
from zope.globalrequest import getRequest
from zope.interface import Invalid, invariant, provider
from zope.lifecycleevent import IObjectAddedEvent, IObjectModifiedEvent
from zope.schema.interfaces import IVocabularyFactory, RequiredMissing

START_SAMPLING_MAPPING = {
    "Y": "1.1.",
    "H1": "1.1.",
    "H2": "1.7.",
    "Q1": "1.1.",
    "Q2": "1.4.",
    "Q3": "1.7.",
    "Q4": "1.10.",
    "M1": "1.1.",
    "M2": "1.2.",
    "M3": "1.3.",
    "M4": "1.4.",
    "M5": "1.5.",
    "M6": "1.6.",
    "M7": "1.7.",
    "M8": "1.8.",
    "M9": "1.9.",
    "M10": "1.10.",
    "M11": "1.11.",
    "M12": "1.12.",
}

STOP_SAMPLING_MAPPING = {
    "Y": "1.1.",
    "H1": "1.7.",
    "H2": "1.1.",
    "Q1": "1.4.",
    "Q2": "1.7.",
    "Q3": "1.10.",
    "Q4": "1.1.",
    "M1": "1.2.",
    "M2": "1.3.",
    "M3": "1.4.",
    "M4": "1.5.",
    "M5": "1.6.",
    "M6": "1.7.",
    "M7": "1.8.",
    "M8": "1.9.",
    "M9": "1.10.",
    "M10": "1.11.",
    "M11": "1.12.",
    "M12": "1.1.",
}


@provider(IFormFieldProvider)
class IREIDoc(IDocumentExtension):

    directives.widget(NuclearInstallations=SelectFieldWidget)
    NuclearInstallations = schema.List(
        title=_("label_rei_NuclearInstallations", default="NuclearInstallations"),
        description=_("description_rei_NuclearInstallation", default=""),
        value_type=schema.Choice(
            source="docpool.rei.vocabularies.NuclearInstallationVocabulary"
        ),
        required=True,
        missing_value=[],
    )
    read_permission(NuclearInstallations="docpool.rei.AccessRei")
    write_permission(NuclearInstallations="docpool.rei.AccessRei")
    searchable("NuclearInstallations")

    directives.widget(ReiLegalBases=CheckBoxFieldWidget)
    ReiLegalBases = schema.List(
        title=_("label_rei_ReiLegalBases", default="ReiLegalBases"),
        description=_("description_rei_ReiLegalBases", default=""),
        value_type=schema.Choice(
            source="docpool.rei.vocabularies.ReiLegalBaseVocabulary"
        ),
        required=True,
        missing_value=[],
    )
    read_permission(ReiLegalBases="docpool.rei.AccessRei")
    write_permission(ReiLegalBases="docpool.rei.AccessRei")
    searchable("ReiLegalBases")

    Medium = schema.Choice(
        title=_("label_rei_Medium", default="Medium"),
        description=_("description_rei_Medium", default=""),
        source="docpool.rei.vocabularies.MediumVocabulary",
        required=False,
    )
    read_permission(Medium="docpool.rei.AccessRei")
    write_permission(Medium="docpool.rei.AccessRei")
    searchable("Medium")

    Year = schema.Choice(
        title=_("label_rei_Year", default="Year"),
        description=_("description_rei_Year", default=""),
        source="docpool.rei.vocabularies.YearVocabulary",
        required=True,
    )
    read_permission(Year="docpool.rei.AccessRei")
    write_permission(Year="docpool.rei.AccessRei")
    searchable("Year")

    Period = schema.Choice(
        title=_("label_rei_Period", default="Period"),
        description=_("description_rei_Period", default=""),
        source="docpool.rei.vocabularies.PeriodVocabulary",
        required=True,
    )
    read_permission(Period="docpool.rei.AccessRei")
    write_permission(Period="docpool.rei.AccessRei")
    searchable("Period")

    directives.widget(Origins=CheckBoxFieldWidget)
    Origins = schema.List(
        title=_("label_rei_Origins", default="Origins"),
        description=_("description_rei_Origin", default=""),
        value_type=schema.Choice(source="docpool.rei.vocabularies.OriginVocabulary"),
        required=True,
        missing_value=[],
    )
    read_permission(Origins="docpool.rei.AccessRei")
    write_permission(Origins="docpool.rei.AccessRei")
    searchable("Origins")

    directives.widget(MStIDs=SelectFieldWidget)
    MStIDs = schema.List(
        title=_(
            "label_rei_MStID", default="Bericht enthält Daten folgender Messstellen"
        ),
        description=_("description_rei_MStID", default=""),
        value_type=schema.Choice(source="docpool.rei.vocabularies.MStIDVocabulary"),
        required=False,
        missing_value=[],
    )
    read_permission(MStIDs="docpool.rei.AccessRei")
    write_permission(MStIDs="docpool.rei.AccessRei")

    mstids_initial_value = schema.TextLine(
        title=_(
            "label_rei_mstids_initial_value",
            default="Bericht enthält Daten folgender Messstellen",
        ),
        required=False,
    )
    directives.omitted("mstids_initial_value")

    directives.widget(Authority=SelectFieldWidget)
    Authority = schema.Choice(
        title=_("label_rei_Authority", default="Authority"),
        description=_("description_rei_Authority", default=""),
        source="docpool.rei.vocabularies.AuthorityVocabulary",
        required=True,
    )
    read_permission(Authority="docpool.rei.AccessRei")
    write_permission(Authority="docpool.rei.AccessRei")
    searchable("Authority")

    PDFVersion = schema.Choice(
        title=_("label_rei_PDFVersion", default="PDF Version"),
        description=_("description_rei_PDFVersion", default=""),
        source="docpool.rei.vocabularies.PDFVersionVocabulary",
        required=True,
        default="keine Angabe",
    )
    directives.mode(PDFVersion="hidden")
    searchable("PDFVersion")

    @invariant
    def validate_medium(data):
        if data.ReiLegalBases and "REI-E" in data.ReiLegalBases:
            if not data.Medium:
                msg = _("For REI-E reports you need to specify a medium.")
                raise Invalid(msg)


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
        if "REI-E" in self.context.ReiLegalBases:
            return self.context.Medium

    @Medium.setter
    def Medium(self, value):
        if "REI-E" in self.context.ReiLegalBases:
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
        day, month, _ = date_fragment.split(".")
        day, month = int(day), int(month)
        year = int(self.Year)
        return date(year=year, month=month, day=day)

    @property
    def StopSampling(self):
        date_fragment = STOP_SAMPLING_MAPPING[self.Period]
        day, month, _ = date_fragment.split(".")
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
        voc = getUtility(
            IVocabularyFactory, "docpool.rei.vocabularies.MStIDVocabulary"
        )()
        return ", ".join(voc.getTerm(i).title for i in getattr(self, "MStIDs", []))

    def period_display(self):
        voc = getUtility(
            IVocabularyFactory, "docpool.rei.vocabularies.PeriodVocabulary"
        )()
        return f"{voc.getTerm(self.Period).title} {self.Year}"

    def nuclear_installations_display(self):
        voc = getUtility(
            IVocabularyFactory, "docpool.rei.vocabularies.NuclearInstallationVocabulary"
        )()
        return ", ".join(voc.getTerm(i).title for i in self.NuclearInstallations)

    def review_history(self):
        # Show WF-History for all users with view-permission.
        # Workaround check for "Review portal content" or "Request review"
        def show_review_history():
            history = self.context.restrictedTraverse("@@review_history")
            return history()

        return execute_under_special_role(self, "Reviewer", show_review_history)

    def authority_display(self):
        voc = getUtility(
            IVocabularyFactory, "docpool.rei.vocabularies.AuthorityVocabulary"
        )()
        return voc.getTerm(self.Authority).title


# IREIDoc sets no marker-interface so we cannot constrain
# the suscriber on IREIDoc. Instead we use IDPDocument
@adapter(IDPDocument, IObjectAddedEvent)
def set_title(obj, event=None):
    if IImportingMarker.providedBy(getRequest()):
        return []

    # Only if it is a IREIDoc.
    try:
        adapted = IREIDoc(obj)
    except Exception:
        return
    legal_base_mapping = {
        "REI-E": "Emissionsbericht",
        "REI-I": "Immissionsbericht",
    }
    if len(adapted.ReiLegalBases) > 1:
        legal = "Immissions- und Emissionsbericht"
    else:
        legal = legal_base_mapping.get(adapted.ReiLegalBases[0])

    period_mapping = {
        "Y": "des {}es",
        "H1": "des {}es",
        "H2": "des {}es",
        "Q1": "des {}s",
        "Q2": "des {}s",
        "Q3": "des {}s",
        "Q4": "des {}s",
        "M1": "{}",
        "M2": "{}",
        "M3": "{}",
        "M4": "{}",
        "M5": "{}",
        "M6": "{}",
        "M7": "{}",
        "M8": "{}",
        "M9": "{}",
        "M10": "{}",
        "M11": "{}",
        "M12": "{}",
    }
    period_vocabulary = getUtility(
        IVocabularyFactory, "docpool.rei.vocabularies.PeriodVocabulary"
    )()
    period_template = period_mapping.get(adapted.Period)
    period_prefix = period_template.format(
        period_vocabulary.getTerm(adapted.Period).title
    )
    period = f"{period_prefix} {adapted.Year}"

    installations = re.split(r", U[A-Z0-9]{3}", adapted.nuclear_installations_display())
    installations[0] = installations[0][5:]
    if len(installations) == 1:
        installations = installations[0]
    elif len(installations) == 2:
        installations = " und ".join(installations)
    else:
        part1 = ", ".join(installations[:-1])
        installations = f"{part1} und {installations[-1]}"
    if "REI-E" in adapted.ReiLegalBases and adapted.Medium:
        medium = f"({adapted.Medium}) "
    else:
        medium = ""
    origins = "({})".format(", ".join(adapted.Origins))
    new_title = "REI-{legal} {medium}{period} {installations} {origins}".format(
        legal=legal,
        period=period,
        installations=installations,
        medium=medium,
        origins=origins,
    )
    obj.title = new_title
    obj.reindexObject(idxs=["Title"])


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
    if getattr(adapted, "mstids_initial_value", None) != value:
        adapted.mstids_initial_value = value

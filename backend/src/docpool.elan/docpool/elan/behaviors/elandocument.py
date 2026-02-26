from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from datetime import datetime
from docpool.base.browser.flexible_view import FlexibleView
from docpool.base.interfaces import IDocumentExtension
from docpool.base.utils import app_only_decorator
from docpool.base.utils import getDocumentPoolSite
from docpool.elan import DocpoolMessageFactory as _
from docpool.elan.config import ELAN_APP
from docpool.elan.utils import getScenariosForCurrentUser
from plone import api
from plone.autoform import directives
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.autoform.interfaces import IFormFieldProvider
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.component import adapter
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


elan_only = app_only_decorator(ELAN_APP)


@provider(IContextAwareDefaultFactory)
def initializeScenario(context):
    query = {
        "portal_type": "DPEvent",
        "UID": getScenariosForCurrentUser(),
        "Status": "active",
    }
    if getattr(context, "dpSearchPath", None):
        query["path"] = context.dpSearchPath()
    scenarios = api.content.find(**query)
    return scenarios[0].UID if scenarios else None


@provider(IFormFieldProvider)
class IELANDocument(IDocumentExtension):
    """ """

    scenario = schema.Choice(
        title=_("label_dpdocument_scenario", default="Belongs to scenario"),
        description=_("description_dpdocument_scenario", default=""),
        required=True,
        source="docpool.elan.vocabularies.Events",
        defaultFactory=initializeScenario,
    )
    read_permission(scenario="docpool.elan.AccessELAN")
    write_permission(scenario="docpool.elan.AccessELAN")
    directives.widget(scenario=RadioFieldWidget)


class ELANDocument(FlexibleView):
    # XXX re #6125: We've seen that accessing ELAN-related attributes on non-ELAN documents may not be
    # well-defined. The simplest measure of defence is to prevent access to ELAN-specific context attributes
    # unless ELAN is supported by the context.
    # (Scenarios might be an empty value or some value that the document had when it used to support ELAN
    # previously, or the attribute might be missing altogether which results in some default being computed by
    # Dexterity.)
    # A better solution would be to prevent adapting a document without support for a particular app to the
    # respective app behavior interface, or have doc_extension() check for app support. This might, however,
    # have more far-reaching consequences (e.g., indexing InfoDocuments elan's category_indexer which happens
    # to be registered for any DPDocument), so at the time of writing this comment, we just go for preventing
    # unsupported attribute access.

    __allow_access_to_unprotected_subobjects__ = 1

    security = ClassSecurityInfo()

    appname = ELAN_APP

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST

    @property
    @elan_only
    def scenario(self):
        # Dexterity overrides __getattr__ to return a default, which is not what we want. hasattr() just calls
        # getattr() so it wouldn't be any help.
        try:
            return self.context.aq_base.__getattribute__("scenario")
        except AttributeError:
            return None

    @scenario.setter
    @elan_only
    def scenario(self, value):
        context = aq_inner(self.context)
        if value != self.scenario:
            context.scenario = value

    def scenarioIndex(self):
        # We can not use the catalog (and therefore, plone.api.content.get()) here since
        # this is used in a indexer and during clear & rebuild no Events would be found.
        # The path of events is assumed to be <docpool>/contentconfig/scen
        # This implicitly filters for events present in the document's docpool but then,
        # other events than those should not be associated with the document anyway.
        if not (scn := self.scenario):
            return

        docpool = getDocumentPoolSite(self.context)
        if not (scen := docpool.unrestrictedTraverse("contentconfig/scen", None)):
            return

        for candidate in scen.contentValues({"portal_type": "DPEvent"}):
            if candidate.UID() == scn and api.content.get_state(candidate) == "published":
                return [scn]

    def getScenarioName(self):
        """ """
        if self.scenario and (scn := api.content.get(UID=self.scenario)):
            return scn.Title

    def category(self):
        """ """
        return self.typeAndCat()[0]

    def typeAndCat(self):
        """ """
        dto = self.context.docTypeObj()
        if dto:
            return dto.title, [self.context.subcategory()]
        return ("", [])


@adapter(IAfterTransitionEvent)
def set_transition_mdate(event):
    if event.transition and event.transition.id != "publish":
        return
    try:
        IELANDocument(event.object)
    except TypeError:
        return
    event.object.mdate = datetime.now()

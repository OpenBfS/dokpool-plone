from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from datetime import datetime
from docpool.base.browser.flexible_view import FlexibleView
from docpool.base.content.dpdocument import IAppSpecificSerializeToJsonDPDocument
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.content.places import IPlaces
from docpool.base.interfaces import IDocumentExtension
from docpool.base.marker import IImportingMarker
from docpool.base.utils import app_only_decorator
from docpool.base.utils import getDocumentPoolSite
from docpool.elan import DocpoolMessageFactory as _
from docpool.elan.config import ELAN_APP
from docpool.elan.content.dpevents import global_events_by_uid
from docpool.elan.utils import get_scenario_for_current_user
from plone import api
from plone.autoform import directives
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.autoform.interfaces import IFormFieldProvider
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.component import adapter
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.interface import named
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory

import logging


log = logging.getLogger(__name__)


elan_only = app_only_decorator(ELAN_APP)


@provider(IContextAwareDefaultFactory)
def initializeScenario(context):
    query = {
        "portal_type": "DPEvent",
        "Status": "active",
    }
    dp_uids = (
        tuple(dp["contentconfig"]["scen"].subscribed_events)
        if (dp := IPlaces(context).document_pool) is not None
        else None
    )
    if (uid := get_scenario_for_current_user(context)) and (dp_uids is None or uid in dp_uids):
        query["UID"] = uid
    elif dp_uids is not None:
        query["UID"] = dp_uids
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
        if IImportingMarker.providedBy(getRequest()):
            return [self.scenario]

        # We can not use the catalog (and therefore, plone.api.content.get()) here since
        # this is used in a indexer and during clear & rebuild no Events would be found.
        # We filter for events subscribed by the document's docpool but then,
        # other events than those should not be associated with the document anyway.
        if not (scn := self.scenario):
            return

        docpool = getDocumentPoolSite(self.context)
        if not (scen := docpool.unrestrictedTraverse("contentconfig/scen", None)):
            return

        if scn not in scen.subscribed_events:
            return

        candidate = global_events_by_uid().get(scn)
        if candidate and api.content.get_state(candidate) == "published":
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
        if doctype_data := self.context.doctype_data():
            return doctype_data["title"], [doctype_data["subcategory"]]
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


@adapter(IDPDocument)
@implementer(IAppSpecificSerializeToJsonDPDocument)
@named(ELAN_APP)
class ELANSpecificSerializeToJsonDPDocument:
    def __init__(self, context):
        self.context = context

    def augment(self, result):
        """Add id of scenario to json used for data-transfer with BW (#5999). Keep lists (#6447)."""
        if "scenario" in result:
            # The lists are left from when there was a list-valued scenarios attribute. We keep them for the
            # time being since this interfaces with external systems. See #6447.
            result["scenarios"] = [scenario := result["scenario"]]
            uid = scenario["token"] if isinstance(scenario, dict) else scenario
            if brains := api.content.find(UID=uid):
                result["scenario_ids"] = [brains[0].id]
        return result

    def receive(self, data):
        if "scenarios" in data:
            data["scenario"] = (scenarios := data["scenarios"])[0]
            if len(scenarios) > 1:
                uids = [s["token"] if isinstance(s, dict) else s for s in scenarios]
                lines = [f"    {s} {'/'.join(api.content.get(UID=s).getPhysicalPath())}" for s in uids]
                log.warning(f"Multiple scenarios for {self.context.getPhysicalPath()}:\n{'\n'.join(lines)}")
        return data

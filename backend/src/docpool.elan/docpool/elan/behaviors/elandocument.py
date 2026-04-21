from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from datetime import datetime
from docpool.base.browser.flexible_view import FlexibleView
from docpool.base.content.doctype import IDocType
from docpool.base.content.dpdocument import IAppSpecificSerializeToJsonDPDocument
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.interfaces import IDocumentExtension
from docpool.base.utils import app_only_decorator
from docpool.base.utils import getDocumentPoolSite
from docpool.elan import DocpoolMessageFactory as _
from docpool.elan.behaviors.elandoctype import IELANDocType
from docpool.elan.config import ELAN_APP
from docpool.elan.utils import getScenariosForCurrentUser
from plone import api
from plone.autoform import directives
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.autoform.interfaces import IFormFieldProvider
from plone.base.utils import safe_text
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import named
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

    def cat_convert(self):
        """ """
        docp = self.context
        while docp.id != "content":
            docp = docp.aq_parent
        docp = docp.aq_parent
        over = docp.esd.overview.title_or_id()
        rec = docp.esd.recent.title_or_id()
        cats = [safe_text(i) for i in self.category()]
        cats = [i for i in cats if i not in [over, rec]]
        cats = "({})".format(", ".join(cats))
        return cats

    def category(self):
        """ """
        return self.typeAndCat()[1]

    def cat_path(self):
        """
        Catalog path for the category object. Needed for a patch to the
        getURL (src/docpool.base/docpool/base/monkey.py) function of brains.
        """
        try:
            doctype_obj = self.context.docTypeObj()
            if doctype_obj:
                category = IELANDocType(doctype_obj).contentCategory
                if category:
                    category_path = category.to_path
                    # Remove the '/Plone/bund/' context path
                    # Todo: Improve
                    return "/".join(category_path.split("/")[3:])
        except BaseException:
            return ""

    def typeAndCat(self):
        """ """
        dto = self.context.docTypeObj()
        if dto:
            if IDocType.providedBy(dto) and IELANDocType(dto, None) is not None:
                return dto.title, IELANDocType(dto).categories()
            else:
                return dto.title, []
        else:
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
        """Add id of scenario to json used for data-transfer with BW (#5999)."""
        if scenario := result.get("scenario"):
            uid = scenario["token"] if isinstance(scenario, dict) else scenario
            if brains := api.content.find(UID=uid):
                # The list is left from when scenarios itself was a list. We keep it for the time being
                # since this interfaces with external systems. See #6447.
                result["scenario_ids"] = [brains[0].id]
        return result

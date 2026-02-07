from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from docpool.base.browser.flexible_view import FlexibleView
from docpool.base.content.doctype import IDocType
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
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


elan_only = app_only_decorator(ELAN_APP)


@provider(IContextAwareDefaultFactory)
def initializeScenarios(context):
    query = {
        "portal_type": "DPEvent",
        "UID": getScenariosForCurrentUser(),
        "Status": "active",
    }
    if getattr(context, "dpSearchPath", None):
        query["path"] = context.dpSearchPath()
    scenarios = api.content.find(**query)
    return [scen.UID for scen in scenarios]


@provider(IFormFieldProvider)
class IELANDocument(IDocumentExtension):
    """ """

    scenarios = schema.List(
        title=_("label_dpdocument_scenarios", default="Belongs to scenarios"),
        description=_("description_dpdocument_scenarios", default=""),
        required=True,
        value_type=schema.Choice(source="docpool.elan.vocabularies.Events"),
        defaultFactory=initializeScenarios,
    )
    read_permission(scenarios="docpool.elan.AccessELAN")
    write_permission(scenarios="docpool.elan.AccessELAN")
    directives.widget(scenarios=CheckBoxFieldWidget)

    scenarios_to_keep = schema.List(
        required=False,
        value_type=schema.TextLine(),
    )
    read_permission(scenarios_to_keep="docpool.elan.AccessELAN")
    directives.mode(scenarios_to_keep="hidden")


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
    def scenarios(self):
        # Dexterity overrides __getattr__ to return a default, which is not what we want. hasattr() just calls
        # getattr() so it wouldn't be any help.
        try:
            return self.context.aq_base.__getattribute__("scenarios")
        except AttributeError:
            return []

    @scenarios.setter
    @elan_only
    def scenarios(self, value):
        scenarios_to_keep = self.request.form.get(
            "form.widgets.IELANDocument.scenarios_to_keep", ""
        ).splitlines()
        new_scenarios = scenarios_to_keep + value
        if not new_scenarios:
            return
        context = aq_inner(self.context)
        context.scenarios = new_scenarios

    @property
    def scenarios_to_keep(self):
        """Inactive scenarios that should be kept referenced when editing.

        There is the feature in editing an ELAN document to hide inactive scenarios from
        the selection of scenarios that may be referenced. By the mechanisms of how
        forms work, this would result in actually removing inactive scenarios from the
        selection. So we need to transport information about these through the edit form
        and count them in when storing the edited form data.
        """
        return [s.UID() for s in self.myScenarioObjects() if s.Status != "active"]

    @scenarios_to_keep.setter
    def scenarios_to_keep(self, value):
        pass

    def isClean(self):
        """
        Is this document free for further action like publishing or transfer.
        @return:
        """
        return self.unknownScenario() is None

    def myScenarioObjects(self):
        """Return DPEvent objects associated with this document."""
        # We can not use the catalog (and therefore, plone.api.content.get()) here since
        # this is used in a indexer and during clear & rebuild no Events would be found.
        # The path of events is assumed to be <docpool>/contentconfig/scen
        # This implicitly filters for events present in the document's docpool but then,
        # other events than those should not be associated with the document anyway.
        results = []
        if not (scns := self.scenarios):
            return results
        docpool = getDocumentPoolSite(self.context)
        if scen := docpool.unrestrictedTraverse("contentconfig/scen", None):
            results = [i for i in scen.contentValues({"portal_type": "DPEvent"}) if i.UID() in scns]
        return results

    def scenarioIndex(self):
        """ """
        scens = self.myScenarioObjects()
        res = [s.UID() for s in scens if api.content.get_state(s) == "published"]
        return res

    def getScenarioNames(self):
        """ """
        # Uniquify titles: While scenarios are UIDs and thus unique, they may
        # refer to events with the same title, most commonly in the case of
        # partly archived events.
        scns = api.content.find(UID=self.scenarios)
        titles = list({brain.Title for brain in scns})
        return titles

    def unknownScenario(self):
        """
        If my scenario is in state private, return it.
        """
        scns = self.myScenarioObjects()
        if scns:
            scn = scns[0]
            sstate = api.content.get_state(scn)
            if sstate == "private":
                return scn
        return None

    def category(self):
        """ """
        return self.typeAndCat()[0]

    def typeAndCat(self):
        """ """
        dto = self.context.docTypeObj()
        if dto:
            return dto.title, [self.context.subcategory()]
        return ("", [])

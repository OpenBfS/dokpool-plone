# -*- coding: utf-8 -*-
from __future__ import print_function
from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from collections import defaultdict
from docpool.base.browser.flexible_view import FlexibleView
from docpool.base.content.doctype import IDocType
from docpool.base.interfaces import IDocumentExtension
from docpool.elan.behaviors.elandoctype import IELANDocType
from docpool.elan.config import ELAN_APP
from docpool.elan import DocpoolMessageFactory as _
from plone import api
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory

import string


@provider(IContextAwareDefaultFactory)
def initializeScenarios(context):
    if not hasattr(context, "getScenariosForCurrentUser"):
        return []

    catalog = getToolByName(context, "portal_catalog")
    scenarios = catalog(
        path=context.dpSearchPath(),
        portal_type='DPEvent',
        UID=context.getScenariosForCurrentUser(),
        Status='active')
    return [scen.id for scen in scenarios]


@provider(IFormFieldProvider)
class IELANDocument(IDocumentExtension):
    """
    """

    scenarios = schema.List(
        title=_(
            u'label_dpdocument_scenarios',
            default=u'Belongs to scenarios'),
        description=_(u'description_dpdocument_scenarios', default=u''),
        required=True,
        value_type=schema.Choice(source="docpool.event.vocabularies.Events"),
        defaultFactory=initializeScenarios,
    )
    read_permission(scenarios='docpool.elan.AccessELAN')
    write_permission(scenarios='docpool.elan.AccessELAN')
    directives.widget(scenarios=CheckBoxFieldWidget)

    scenarios_to_keep = schema.List(
        required=False,
        value_type=schema.TextLine(),
    )
    read_permission(scenarios_to_keep='docpool.elan.AccessELAN')
    directives.mode(scenarios_to_keep='hidden')


class ELANDocument(FlexibleView):

    __allow_access_to_unprotected_subobjects__ = 1

    security = ClassSecurityInfo()

    appname = ELAN_APP

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST

    @property
    def scenarios(self):
        return self.context.scenarios

    @scenarios.setter
    def scenarios(self, value):
        scenarios_to_keep = self.request.form.get(
            'form.widgets.IELANDocument.scenarios_to_keep', '').splitlines()
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
        return [s.id for s in self.myScenarioObjects() if s.Status != 'active']

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
        """
        """
        cat = getToolByName(self.context, "portal_catalog")
        scns = getattr(self.context, "scenarios", [])
        return [
            s.getObject()
            for s in cat(
                path=self.context.dpSearchPath(), portal_type='DPEvent', getId=scns
            )
        ]

    def scenarioIndex(self):
        """
        """
        scens = self.myScenarioObjects()
        res = [
            scen.getId()
            for scen in scens
            if api.content.get_state(scen) == u'published'
        ]
        return res

    def debugvalues(self):
        """
        """
        print(self.context.scenarios)
        print(self.context.docType)

    def getScenarioNames(self):
        """
        """
        cat = getToolByName(self.context, "portal_catalog")
        scns = self.scenarios
        # FIXME: As long as events are referenced by id, which may not be unique,
        # uniquify titles: for each id, use distinct titles of non-archived events
        # or, failing that, of archived events. Sounds like a reasonable compromise
        # between general applicability and catering to the most likely use case of
        # a single partly archived event.
        brains_by_id = defaultdict(list)
        for b in cat(
            path=self.context.dpSearchPath(), portal_type='DPEvent', getId=scns
        ):
            brains_by_id[b.getId].append(b)
        titles = []
        for id, brains in brains_by_id.items():
            active = [b for b in brains if '/archive' not in b.getPath()]
            titles.extend(set(b.Title for b in active or brains))
        return titles

    def unknownScenario(self):
        """
        If my scenario is in state private, return it.
        """
        scns = self.myScenarioObjects()
        if scns:
            scn = scns[0]
            sstate = api.content.get_state(scn)
            if sstate == 'private':
                return scn
        return None

    def cat_convert(self):
        """
        """
        docp = self.aq_parent
        while docp.id != 'content':
            docp = docp.aq_parent
        docp = docp.aq_parent
        over = docp.esd.overview.title_or_id()
        rec = docp.esd.recent.title_or_id()
        cats = [safe_unicode(i) for i in self.category()]
        cats = [i for i in cats if i not in [over, rec]]
        cats = u'({0})'.format(u', '.join(cats))
        return cats

    def category(self):
        """
        """
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
        """
        """
        #        print self
        dto = self.context.docTypeObj()
        if dto:
            #            print dto
            if IDocType.providedBy(dto):
                return dto.title, IELANDocType(dto).categories()
            else:
                return dto.title, []
        else:
            return ("", [])

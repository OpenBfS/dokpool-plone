# -*- coding: utf-8 -*-
from __future__ import print_function
from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from docpool.base.browser.flexible_view import FlexibleView
from docpool.base.content.doctype import IDocType
from docpool.base.interfaces import IDocumentExtension
from docpool.elan.behaviors.elandoctype import IELANDocType
from docpool.elan.config import ELAN_APP
from elan.esd import DocpoolMessageFactory as _
from plone import api
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives
from Products.CMFCore.utils import getToolByName
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory

import string


@provider(IContextAwareDefaultFactory)
def initializeScenarios(context):
    if hasattr(context, "getUserSelectedScenarios"):
        return context.getUserSelectedScenarios()
    else:
        return []


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

    def _get_scenarios(self):
        return self.context.scenarios

    def _set_scenarios(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        scenarios_to_keep = self.request.form.get(
            'form.widgets.IELANDocument.scenarios_to_keep', '').splitlines()
        context.scenarios = scenarios_to_keep + value

    scenarios = property(_get_scenarios, _set_scenarios)

    @property
    def scenarios_to_keep(self):
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
        return [
            s.Title
            for s in cat(
                path=self.context.dpSearchPath(), portal_type='DPEvent', getId=scns
            )
        ]

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
        cats = ''
        for c in self.category():
            if c not in [over, rec] and c.encode('utf') not in [over, rec]:
                cats = cats + c + ', '
        cats = '(' + cats + ')'
        cats = string.replace(cats, ', )', ')')
        return cats

    def category(self):
        """
        """

        return self.typeAndCat()[1]

    def cat_path(self):
        """
        Catalog path for the category object. Needed for a patch to the getURL function of brains.
        """
        # print "cat_path"
        try:
            dto = self.context.docTypeObj()
            if dto:
                # print "DTO"
                # print dto.Title()
                cat = IELANDocType(dto).contentCategory
                if cat:
                    aup = cat.to_path
                    # print aup
                    aup = "/".join(aup.split("/")[4:])
                    return aup
                # print "no cat"
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

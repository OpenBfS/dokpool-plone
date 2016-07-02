# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo

from plone.autoform.directives import read_permission, write_permission
from zope.interface import provider, implementer
from zope.component import adapter
from plone.autoform.interfaces import IFormFieldProvider

from docpool.elan.config import ELAN_APP
from elan.esd.behaviors.transferable import ITransferable, Transferable
from zope import schema
from plone.supermodel import model
from plone.directives import form
from z3c.relationfield.schema import RelationChoice, RelationList
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from plone.indexer.interfaces import IIndexer
from Products.ZCatalog.interfaces import IZCatalog
from Products.CMFCore.utils import getToolByName
from plone import api
from elan.esd import DocpoolMessageFactory as _
from elan.esd.behaviors.elandoctype import IELANDocType
from zope.interface.interface import Interface
from Acquisition import aq_inner
from docpool.base.content.doctype import IDocType

@provider(IFormFieldProvider)
class IELANDocument(model.Schema):
    """
    """
    scenarios = schema.List(
        title=_(u'label_dpdocument_scenarios', default=u'Belongs to scenarios'),
        description=_(u'description_dpdocument_scenarios', default=u''),
        required=True,
        value_type=schema.Choice(source="elan.esd.vocabularies.Scenarios"),
    )
    read_permission(scenarios='docpool.elan.AccessELAN')
    write_permission(scenarios='docpool.elan.AccessELAN')
    form.widget(scenarios=CheckBoxFieldWidget)


@form.default_value(field=IELANDocument['scenarios'])
def initializeScenarios(data):
    if hasattr(data.context, "getUserSelectedScenarios"):
        return data.context.getUserSelectedScenarios()
    else:
        return []



class ELANDocument(object):
    
    __allow_access_to_unprotected_subobjects__ = 1
    
    security = ClassSecurityInfo()
    
    def __init__(self, context):
        self.context = context

    def _get_scenarios(self):
        return self.context.extension(ELAN_APP).scenarios

    def _set_scenarios(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.extension(ELAN_APP).scenarios = value
    
    scenarios = property(_get_scenarios, _set_scenarios)
    

    



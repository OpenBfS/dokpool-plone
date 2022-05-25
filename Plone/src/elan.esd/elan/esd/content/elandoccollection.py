# -*- coding: utf-8 -*-
#
# File: elandoccollection.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

from __future__ import print_function
__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the ELANDocCollection content type. See elandoccollection.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.elan.config import ELAN_APP
from docpool.event.utils import getScenariosForCurrentUser
from elan.esd import DocpoolMessageFactory as _
from elan.esd.utils import getCategoriesForCurrentUser
from plone.app.contenttypes.content import Collection
from plone.app.contenttypes.content import ICollection
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.supermodel import model
from plone.protect.interfaces import IDisableCSRFProtection
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_encode
from z3c.relationfield.event import updateRelations
from z3c.relationfield.relation import RelationValue
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.component import adapter
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent


class IELANDocCollection(model.Schema, ICollection):
    """
    """

    docTypes = RelationList(
        title=_(
            u'label_elandoccollection_doctypes',
            default=u'Document Types'),
        description=_(u'description_elandoccollection_doctypes', default=u''),
        required=False,
        value_type=RelationChoice(
            title=_("Document Types"), source="docpool.base.vocabularies.DocType"
        ),
    )

    directives.widget(docTypes='z3c.form.browser.select.CollectionSelectFieldWidget')


#    directives.widget(docTypes=AutocompleteMultiFieldWidget)


@implementer(IELANDocCollection)
class ELANDocCollection(Item, Collection):
    """
    """

    security = ClassSecurityInfo()

    def testSearch(self):
        """
        """
        kw = {
            'portal_type': {'query': ['DPDocument']},
            'sort_on': 'mdate',
            'dp_type': {'query': ['eventinformation', 'nppinformation']},
            'scenarios': {'query': ['scenario2', 'scenario1']},
            'sort_order': 'reverse',
            'path': {'query': '/Plone/Members'},
        }
        res = self.portal_catalog(**kw)
        # print len(res)
        for r in res:
            print(r.Title)

    def getUserSelectedScenarios(self):
        """
        """
        uss = getScenariosForCurrentUser(self)
        # print usc
        return uss

    def getUserSelectedCategories(self):
        """
        """
        usc = getCategoriesForCurrentUser(self)
        # print usc
        return usc

    def results(self, batch=True, b_start=0,
                b_size=10, sort_on=None, brains=False):
        """Get results override, implicit = True"""
        if sort_on is None:
            sort_on = self.sort_on
        return self.getQuery(
            implicit=True,
            batch=batch,
            b_start=b_start,
            b_size=b_size,
            sort_on=sort_on,
            brains=brains,
        )

    def correctDocTypes(self):
        """
        Replace references to global doc types with references to local doc types.
        """
        request = self.REQUEST
        alsoProvides(request, IDisableCSRFProtection)
        dts = self.docTypes
        res = []
        intids = getUtility(IIntIds)
        if dts:
            for dt in dts:
                t = dt.to_object
                new = None
                if t:
                    tid = t.getId()
                    try:
                        new = self.config.dtypes[tid]
                    except BaseException:
                        pass
                    if new:
                        to_id = intids.getId(new)
                        res.append(RelationValue(to_id))

            self.docTypes = res
            updateRelations(self, None)
            self.setDocTypesUpdateCollection()
            self.reindexObject()

    def setDocTypesUpdateCollection(self, values=None):
        """
        Update the criteria for the underlying collection.
        """
        if values:
            self.docTypes = values

        # We always search for ELAN content
        params = [
            {
                'i': 'portal_type',
                'o': 'plone.app.querystring.operation.selection.is',
                'v': ['DPDocument', 'SituationReport', 'SRModule'],
            }
        ]
        # We usually also have document types configured
        # This returns the corresponding Type Object(s)
        types = self.docTypes
        if types:
            params.append(
                {
                    'i': 'dp_type',
                    'o': 'plone.app.querystring.operation.selection.is',
                    'v': [t.to_object.getId() for t in types if t.to_object],
                }
            )  # getId() vorher

        self.query = params
        self.sort_on = 'changed'
        self.sort_reversed = True

    def isOverview(self):
        """
        Is this an overview collection?
        """
        return self.getId().find('overview') > -1

    def dp_type(self):
        """
        We use this index to mark those collections which actually serve as categories.
        """
        # print self
        if self.docTypes:
            #    print "active"
            return "active"
        else:
            #    print "inactive"
            return "inactive"

    security.declareProtected(View, 'synContentValues')

    def synContentValues(self):
        """Getter for syndycation support
        """
        syn_tool = getToolByName(self, 'portal_syndication')
        limit = int(syn_tool.getMaxItems(self))
        return self.getQuery(batch=False, brains=True, limit=limit)[:limit]

    def getQuery(self, **kwargs):
        """Get the query dict from the request or from the object"""
        from zope.site.hooks import getSite
        from plone.app.querystring.querybuilder import QueryBuilder

        # print "modified get"
        request = self.REQUEST
        alsoProvides(request, IDisableCSRFProtection)
        raw = kwargs.get('raw', None)
        implicit_filter = kwargs.get('implicit', False)
        value = self.query  # .raw
        if not value:
            self.setDocTypesUpdateCollection()  # Not yet initialized
            value = self.query
        # print value
        if raw == True:
            # We actually wanted the raw value, should have called getRaw
            return value
        querybuilder = QueryBuilder(self, getSite().REQUEST)

        if implicit_filter:
            # Not in the archive:
            value = list(value[:])  # Otherwise we change the stored query!
            if not self.restrictedTraverse("@@context_helpers").is_archive():
                # First implicit filter: the user has select scenario(s) as a
                # filter
                uss = self.getUserSelectedScenarios()
                if uss:
                    # This is THE modification: append the implicit criterion
                    # for the scenario(s)
                    value.append(
                        {
                            'i': 'scenarios',
                            'o': 'plone.app.querystring.operation.selection.is',
                            'v': uss,
                        }
                    )
                else:  # If nothing selected, don't show results!
                    value.append(
                        {
                            'i': 'scenarios',
                            'o': 'plone.app.querystring.operation.selection.is',
                            'v': ["dontfindanything"],
                        }
                    )
                    # print value
            # Second implicit filter: the user has selected categories as a filter
            # Used for the chronological overview
            if self.isOverview():
                usc = self.getUserSelectedCategories()
                if usc:
                    value.append(
                        {
                            'i': 'category',
                            'o': 'plone.app.querystring.operation.selection.is',
                            'v': [safe_encode(i) for i in usc],
                        }
                    )

            # Third implicit filter: only results with ELAN support are wanted.
            value.append(
                {
                    'i': 'apps_supported',
                    'o': 'plone.app.querystring.operation.selection.is',
                    'v': [ELAN_APP],
                }
            )

            # Now we restrict the search to the paths to Members and Groups.
            # This ensures that in case of archives we only get results from the correct subset.
            # m = self.content

            # mpath = getRelativePath(m)
            mpath = "content"
            # Just one path allowed in the path criterion. Must be the part
            # after the portal root, e.g. '/Members'
            value.append(
                {
                    'i': 'path',
                    'o': 'plone.app.querystring.operation.string.path',
                    'v': "/%s" % mpath,
                }
            )

        sort_on = kwargs.get('sort_on', self.sort_on)
        sort_order = 'reverse' if self.sort_reversed else 'ascending'
        limit = kwargs.get('limit', self.limit)
        # print value
        res = querybuilder(
            query=value,
            batch=kwargs.get('batch', False),
            b_start=kwargs.get('b_start', 0),
            b_size=kwargs.get('b_size', 30),
            sort_on=sort_on,
            sort_order=sort_order,
            limit=limit,
            brains=kwargs.get('brains', False),
        )
        # print len(res)
        return res


@adapter(IELANDocCollection, IObjectModifiedEvent)
def update_docTypes(obj, event=None):
    """
    """
    if obj:
        # print "update_docTypes", obj.docTypes
        obj.setDocTypesUpdateCollection()
        obj.reindexObject()


@adapter(IELANDocCollection, IObjectAddedEvent)
def enableSyndication(obj, event=None):
    syn_tool = getToolByName(obj, 'portal_syndication', None)
    if syn_tool is not None:
        if syn_tool.isSiteSyndicationAllowed() and not syn_tool.isSyndicationAllowed(
            obj
        ):
            syn_tool.enableSyndication(obj)

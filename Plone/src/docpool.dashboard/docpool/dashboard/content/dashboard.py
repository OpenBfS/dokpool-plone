# -*- coding: utf-8 -*-
#
# File: dashboard.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the Dashboard content type. See dashboard.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.dashboard import DocpoolMessageFactory as _
from plone.dexterity.content import Item
from plone.directives import form
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.interface import implements


class IDashboard(form.Schema):
    """
    """

    dbCollections = RelationList(
        title=_(u'label_dashboard_dbcollections', default=u'Document Types'),
        description=_(
            u'description_dashboard_dbcollections',
            default=u'Select the document types you want to show in this dashboard.',
        ),
        required=False,
        value_type=RelationChoice(
            title=_("Document Types"),
            source="docpool.dashboard.vocabularies.DashboardCollections",
        ),
    )

    form.widget(dbCollections='z3c.form.browser.select.CollectionSelectFieldWidget')


class Dashboard(Item):
    """
    """

    security = ClassSecurityInfo()

    implements(IDashboard)

    def currentDocuments(self):
        """
        Loop through all configured collections,
        get the most recent document (if available).
        """
        res = []
        for c in self.dbCollections and self.dbCollections or []:
            coll = c.to_object
            docs = coll.results(b_size=1)
            if len(docs) > 0:
                res.append((coll.Title(), docs[0]))
            else:
                res.append((coll.Title(), None))
        #        print res
        return res

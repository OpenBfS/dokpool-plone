# -*- coding: utf-8 -*-
#
# File: situationoverview.py
#
# Copyright (c) 2017 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the SituationOverview content type. See situationoverview.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from docpool.base.utils import queryForObject
from docpool.base.utils import queryForObjects
from docpool.elan.config import ELAN_APP
from docpool.event.utils import getScenarioIdsForCurrentUser
from elan.sitrep import DocpoolMessageFactory as _
from elan.sitrep.vocabularies import ModuleTypesVocabularyFactory
from plone.dexterity.content import Item
from plone.supermodel import model
from Products.CMFPlone.utils import safe_unicode
from zope.interface import implementer


class ISituationOverview(model.Schema):
    """
    """


@implementer(ISituationOverview)
class SituationOverview(Item):
    """
    """

    security = ClassSecurityInfo()

    APP = ELAN_APP

    def modTypes(self):
        """
        """
        return ModuleTypesVocabularyFactory(self, raw=True)

    def availableSituationReports(self):
        """
        For every situation report:
        * Get all modules that belong to it
        * Determine "missing" modules
        """
        uss = getScenarioIdsForCurrentUser(self)
        path = self.dpSearchPath()
        reports = queryForObjects(
            self,
            path=path,
            portal_type='SituationReport',
            sort_on='changed',
            sort_order='reverse',
            review_state='published',
            changed={
                'query': (DateTime() - 14).asdatetime().replace(tzinfo=None),
                'range': 'min',
            },
            scenarios=uss,
        )
        # mtypes = self.modTypes()
        res1 = []
        res2 = {}
        for report in [r.getObject() for r in reports]:
            # mods = {}
            # for mt in mtypes:
            #    mods[mt[0]] = None
            # ms = report.myModules()
            # for m in ms:
            #    mods[m.docType] = m
            # res2[report.UID()] = ( report, mods )
            res1.append(
                (
                    report.UID(),
                    "%s %s"
                    % (
                        safe_unicode(report.Title()),
                        self.toLocalizedTime(
                            DateTime(
                                report.changed()),
                            long_format=1),
                    ),
                )
            )
        default = [("", _("Current situation"))]
        ud = [("userdefined", _("User defined"))]
        return default + res1 + ud, res2

    def availableModules(self, reportUID=None):
        """
        For every module type:
        * Get all published modules (back two weeks)
        * Only for the currently selected events.
        * Check if there is a private version of the module newer that the latest published version.
        * Optional: check if that version is currently locked.
        If reportUID is given, determine the UIDs for that report's modules, otherwise determine the UID of the
        most recent module for each type.
        """
        return _availableModules(self, reportUID)

    def modinfo(self, moduid=None):
        """
        """
        if moduid:
            module = queryForObject(self, UID=moduid)
            if module:
                return module.restrictedTraverse("@@info")()
        return _("No content found")


def _availableModules(self, reportUID=None):
    res = {}
    moduids = {}
    uss = getScenarioIdsForCurrentUser(self)
    path = self.dpSearchPath()

    for mt in self.modTypes():
        moduids[mt[0]] = None
        mods = queryForObjects(
            self,
            path=path,
            dp_type=mt[0],
            portal_type='SRModule',
            sort_on='changed',
            sort_order='reverse',
            review_state='published',
            changed={
                'query': (DateTime() - 14).asdatetime().replace(tzinfo=None),
                'range': 'min',
            },
            scenarios=uss,
        )
        modres = [
            (
                m.UID,
                u"%s %s"
                % (
                    safe_unicode(m.Title),
                    self.toLocalizedTime(DateTime(m.changed), long_format=1),
                ),
            )
            for m in mods
        ]
        latest = (
            mods
            and mods[0].changed
            or (DateTime() - 14).asdatetime().replace(tzinfo=None)
        )
        if mods:
            moduids[mt[0]] = mods[0].UID
        current = queryForObjects(
            self,
            path=path,
            dp_type=mt[0],
            portal_type='SRModule',
            sort_on='changed',
            sort_order='reverse',
            review_state='private',
            changed={'query': latest, 'range': 'min'},
            scenarios=uss,
        )
        if current:
            current = current[0].getObject()
        else:
            current = None
        res[mt[0]] = (modres, current)
    if reportUID:
        report = queryForObject(self, UID=reportUID)
        if report:
            ms = report.myModules()
            for m in ms:
                moduids[m.docType] = m.UID()
    return res, moduids

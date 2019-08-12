from zope.interface import Interface, implements

from Acquisition import aq_inner
from Acquisition import aq_parent


from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import getToolByName
from Products.ZCatalog.ZCatalog import ZCatalog
from Products.CMFPlone.CatalogTool import CatalogTool

from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides


class ISRCatalog(Interface):
    """
    """


class SRCatalog(CatalogTool):
    """
    A specific SR catalog tool
    """

    implements(ISRCatalog)

    title = 'Situation Report Catalog'
    id = 'sr_catalog'
    portal_type = meta_type = 'SRCatalog'
    plone_tool = 1

    security = ClassSecurityInfo()
    _properties = ({'id': 'title', 'type': 'string', 'mode': 'w'},)

    def __init__(self):
        ZCatalog.__init__(self, self.id)

    security.declarePublic('enumerateIndexes')

    def enumerateIndexes(self):
        """Returns indexes used by catalog"""
        return (
            ('id', 'FieldIndex', ()),
            ('portal_type', 'FieldIndex', ()),
            ('path', 'ExtendedPathIndex', ('getPhysicalPath')),
            ('getCanonicalPath', 'ExtendedPathIndex', ('getCanonicalPath')),
            ('scenarios', 'KeywordIndex', ('getSRScenarioNames')),
            ('phases', 'KeywordIndex', ('getSRPhaseNames')),
            ('modules', 'KeywordIndex', ('getSRModuleNames')),
            ('scenarioRefs', 'KeywordIndex', ('getSRScenarioRefs')),
            ('phaseRefs', 'KeywordIndex', ('getSRPhaseRefs')),
            ('moduleRefs', 'KeywordIndex', ('getSRModuleRefs')),
            ('review_state', 'FieldIndex', ()),
            ('sortable_title', 'FieldIndex', ()),
            ('allowedRolesAndUsers', 'DPLARAUIndex', ()),
        )

    security.declareProtected(ManagePortal, 'clearFindAndRebuild')

    def clearFindAndRebuild(self):
        """Empties catalog, then finds all contentish objects (i.e. objects
           with an indexObject method), and reindexes them.
           This may take a long time.
        """
        request = self.REQUEST
        alsoProvides(request, IDisableCSRFProtection)

        self.manage_catalogClear()

        cat = getToolByName(self, 'portal_catalog')
        # FIXME: Probably only SRTextBlock is needed here...
        brains = cat(
            {
                'portal_type': (
                    "SRScenario",
                    "SRPhase",
                    "SRModuleConfig",
                    "SRTextBlock",
                    "SituationReport",
                    "SRModule",
                )
            }
        )
        for brain in brains:
            obj = brain.getObject()
            if obj:
                self._reindexObject(obj)


InitializeClass(SRCatalog)

# -*- coding:utf-8 -*-
from elan.journal.interfaces import IJournal
from elan.journal.logger import logger
from ftw.upgrade.workflow import WorkflowChainUpdater
from plone import api


def migrate_journal_workflow(context):
    """Migrate journal workflow."""
    review_state_mapping = {
        ('journal_workflow', 'simple_publication_workflow'): {
            'private': 'private',
            'active': 'published',
            'inactive': 'published',
        }
    }

    catalog = api.portal.get_tool('portal_catalog')
    query = dict(object_provides=IJournal.__identifier__)
    results = catalog.unrestrictedSearchResults(**query)
    objects = (b.getObject() for b in results)

    # all existing journals must use now simple_publication_workflow
    wtool = api.portal.get_tool('portal_workflow')
    with WorkflowChainUpdater(objects, review_state_mapping):
        wtool.setChainForPortalTypes(('Journal',), ('simple_publication_workflow',))
        logger.info('Journal objects now use simple_publication_workflow')

    # remove journal_workflow
    if 'journal_workflow' in wtool:
        api.content.delete(obj=wtool.journal_workflow)
        logger.info('Journal workflow removed')

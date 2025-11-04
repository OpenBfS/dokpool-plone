from plone import api
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost
from Products.Sessions.BrowserIdManager import BrowserIdManager
from Products.Sessions.SessionDataManager import SessionDataManager
from Products.TemporaryFolder.TemporaryFolder import MountedTemporaryFolder
from Products.Transience.Transience import TransientObjectContainer
from zope.component import getSiteManager

import transaction


def mock_mail_host(portal):
    api.portal.set_registry_record("plone.email_from_name", "hallo@welt.de")
    api.portal.set_registry_record("plone.email_from_address", "hallo@welt.de")
    portal._original_mailhost = portal.MailHost
    portal.MailHost = mailhost = MockMailHost("MailHost")
    sm = getSiteManager(context=portal)
    sm.unregisterUtility(provided=IMailHost)
    sm.registerUtility(mailhost, provided=IMailHost)

    transaction.commit()


def setup_sdm(portal):
    """Setup session data manager
    stolen from plone.app.contenttypes.tests.test_migration.MigrationFunctionalTests.test_atct_migration_form  # noqa
    """
    tf_name = "temp_folder"
    idmgr_name = "browser_id_manager"
    toc_name = "temp_transient_container"
    sdm_name = "session_data_manager"
    bidmgr = BrowserIdManager(idmgr_name)
    tf = MountedTemporaryFolder(tf_name, title="Temporary Folder")
    toc = TransientObjectContainer(toc_name, title="Temporary Transient Object Container", timeout_mins=20)
    session_data_manager = SessionDataManager(
        id=sdm_name,
        path=tf_name + "/" + toc_name,
        title="Session Data Manager",
        requestName="SESSION",
    )
    app = portal.__parent__
    app._setObject(idmgr_name, bidmgr)
    app._setObject(sdm_name, session_data_manager)
    app._setObject(tf_name, tf)
    app.temp_folder._setObject(toc_name, toc)
    transaction.commit()

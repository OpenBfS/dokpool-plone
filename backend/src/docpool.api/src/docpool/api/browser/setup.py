from Acquisition import aq_get
from datetime import datetime
from datetime import timedelta
from eea.facetednavigation.config import ANNO_FACETED_LAYOUT
from eea.facetednavigation.layout.interfaces import IFacetedLayout
from elan.journal.tests.utils import _create_journalentries
from plone import api
from plone.app.textfield import RichTextValue
from plone.dexterity.events import EditFinishedEvent
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from plone.protect.interfaces import IDisableCSRFProtection
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import WorkflowPolicyConfig_id
from Products.CMFPlone.utils import get_installer
from Products.Five.browser import BrowserView
from Products.GenericSetup.context import SnapshotImportContext
from Products.GenericSetup.interfaces import IBody
from z3c.relationfield.relation import RelationValue
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from zope.component import queryUtility
from zope.component._api import queryMultiAdapter
from zope.event import notify
from zope.globalrequest import getRequest
from zope.interface import alsoProvides
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import modified
from zope.schema.interfaces import IVocabularyFactory

import logging
import os
import random


log = logging.getLogger(__name__)


def dummy_image(filename="image.png"):
    file_ = os.path.join(os.path.dirname(__file__), filename)
    with open(file_, "rb") as fd:
        data = fd.read()
    return NamedBlobImage(data=data, filename=filename)


def dummy_file(filename="file.pdf"):
    file_ = os.path.join(os.path.dirname(__file__), filename)
    with open(file_, "rb") as fd:
        data = fd.read()
    return NamedBlobFile(data=data, filename=filename)


class DocpoolSetup(BrowserView):
    """Setup some content useful for testing

    * Installs addons elan and doksys plus many dependencies
    * Create two docpools (b8nd and bayern)
    * Add a user tester:tester that can write into bund and read bayern
    * Create demo-content into bund/


    """

    def __call__(self):
        if not self.request.form.get("submit", None):
            return self.index()

        alsoProvides(self.request, IDisableCSRFProtection)

        # install addons
        installer = get_installer(self.context, self.request)
        installer.install_product("docpool.config")
        installer.install_product("docpool.doksys")
        installer.install_product("elan.journal")
        installer.install_product("docpool.rei")

        api.portal.set_registry_record("docpool.show_debug_info", True)

        # remove My Folder action added by set_enable_user_folders of addons
        portal_actions = api.portal.get_tool("portal_actions")
        user_actions = getattr(portal_actions, "user")
        if "mystuff" in user_actions:
            user_actions.manage_delObjects(["mystuff"])

        # Sort actions
        actions = [
            "add_scenario",
            "edit_scenarios",
            "edit_ticker",
            "delete_ticker",
            "edit_dashboard",
            "plone_setup",
            "usermanagement",
            "impersonate",
            "preferences",
            "logout",
        ]
        for action in actions:
            user_actions.moveObjectsToBottom([action])

        # create docpool 1 (with rei)
        docpool_bund = api.content.create(
            container=self.context,
            type="DocumentPool",
            id="bund",
            title="Bund",
            prefix="bund",
            supportedApps=("elan", "doksys", "rei"),
            exclude_from_nav=False,
        )
        notify(EditFinishedEvent(docpool_bund))
        log.info("Created docpool bund")

        # create docpool 2 (without rei)
        docpool_land = api.content.create(
            container=self.context,
            type="DocumentPool",
            id="hessen",
            title="Hessen",
            prefix="hessen",
            supportedApps=("elan", "doksys"),
            exclude_from_nav=False,
        )
        notify(EditFinishedEvent(docpool_land))
        log.info("Created docpool hessen")

        user1 = add_user(docpool_bund, "user1", ["group1"])
        log.info("Created user1 and group1 in docpool bund")
        user2 = add_user(
            docpool_land, "user2", ["group2"], enabled_apps=["elan", "doksys"]
        )
        log.info("Created user2 and group2 in docpool hessen")

        # Setup REI Users and groups for hessen and bayern
        log.info("Creating Groups for REI")
        add_user(docpool_bund, "aufsicht_he", ["aufsicht_he"], enabled_apps=["rei"])
        add_user(docpool_bund, "betreiber_he", ["betreiber_he"], enabled_apps=["rei"])
        add_user(docpool_bund, "aufsicht_by", ["aufsicht_by"], enabled_apps=["rei"])

        # Add group bund_aufsicht that contains all aufsicht groups
        # this group has no defaul-user. use the aufsicht users to test it.
        bund_aufsicht = add_group(docpool_bund, "aufsicht")
        bund_aufsicht.setProperties({"allowedDocTypes": []})
        portal_groups = api.portal.get_tool("portal_groups")
        portal_groups.addPrincipalToGroup("bund_aufsicht_he", "bund_aufsicht")
        portal_groups.addPrincipalToGroup("bund_aufsicht_by", "bund_aufsicht")

        # Add REI users and groups for bund
        add_user(docpool_bund, "bmu_rei", ["bmu_rei"], enabled_apps=["rei"])
        add_user(docpool_bund, "bfs_rei", ["bfs_rei"], enabled_apps=["rei"])

        # Configure REI-group-folders
        groups_folder = docpool_bund["content"]["Groups"]

        group = api.group.get("bund_aufsicht_he")
        # This group can only add rei-reports
        group.setProperties({"allowedDocTypes": ["reireport"]})
        group_folder = groups_folder["bund_aufsicht_he"]
        group_folder.allowedDocTypes = ["reireport"]
        group_folder.reindexObject()
        # The folders for the creators of reireports have a custom workflow
        set_placeful_workflow(group_folder, "rei_he1")

        group = api.group.get("bund_betreiber_he")
        group.setProperties({"allowedDocTypes": ["reireport"]})
        group_folder = groups_folder["bund_betreiber_he"]
        group_folder.allowedDocTypes = ["reireport"]
        group_folder.reindexObject()
        # For Hessen Aufsicht and Betreiber can add reports!
        set_placeful_workflow(group_folder, "rei_he2")

        group = api.group.get("bund_aufsicht_by")
        group.setProperties({"allowedDocTypes": ["reireport"]})
        group_folder = groups_folder["bund_aufsicht_by"]
        group_folder.allowedDocTypes = ["reireport"]
        group_folder.reindexObject()
        # For Bayern only Aufsicht can add reports!
        set_placeful_workflow(group_folder, "rei_by")

        # The gloabl groups do not create content.
        group = api.group.get("bund_aufsicht")
        group.setProperties({"allowedDocTypes": []})
        group_folder = groups_folder["bund_aufsicht"]
        group_folder.reindexObject()

        group = api.group.get("bund_bmu_rei")
        group.setProperties({"allowedDocTypes": []})
        group_folder = groups_folder["bund_bmu_rei"]
        group_folder.reindexObject()

        group = api.group.get("bund_bfs_rei")
        group.setProperties({"allowedDocTypes": []})
        group_folder = groups_folder["bund_bfs_rei"]
        group_folder.reindexObject()

        # get the content-folder for a group to test with
        folder = docpool_bund["content"]["Groups"]["bund_group1"]

        voc = getUtility(IVocabularyFactory, name="docpool.base.vocabularies.DocType")
        doctypes = voc(self.context, raw=True)

        event_config_folder = docpool_bund["contentconfig"]["scen"]
        dpnuclearpowerstation = api.content.create(
            container=event_config_folder,
            type="DPNuclearPowerStation",
            id="kernkraftwerk-1",
            title="Kernkraftwerk 1",
            coordinates="POINT(12.240313700000002 48.59873489999998)",
            exclude_from_nav=False,
        )
        log.info("Created dpnuclearpowerstation")
        dpnetwork = api.content.create(
            container=event_config_folder,
            type="DPNetwork",
            id="testnetz",
            title="Testnetz",
            coordinates="POLYGON((12.789515693194565 48.70897536061274,11.9394485546417 48.750643880797945,11.725215156233618 48.447309003359074,12.352809150286648 48.38076862235553,12.803248603348985 48.39080082760333,12.789515693194565 48.70897536061274))",
            exclude_from_nav=False,
        )
        log.info("Created dpnetwork")
        dpevent = api.content.create(
            container=event_config_folder,
            type="DPEvent",
            id="test-event",
            title="Test Event",
            description="Die Beschreibung",
            EventType="Exercise",
            Status="active",
            AlertingStatus="none",
            AreaOfInterest="POLYGON((12.124842841725044 48.60077830054228,12.157801826095657 48.51533914735478,12.702998359223052 48.63164629148582,12.865046699043434 48.77393903963252,12.124842841725044 48.60077830054228))",
            EventCoordinates="POINT(12.240313700000002 48.59873489999998)",
            EventLocation=RelationValue(get_intid(dpnuclearpowerstation)),
            SectorizingNetworks=[RelationValue(get_intid(dpnetwork))],
            EventPhase=None,
            Exercise=True,
            TimeOfEvent=datetime.now(),
            OperationMode="routine",
            SectorizingSampleTypes=[
                "A",
                "A1",
                "A2",
                "A3",
            ],
            exclude_from_nav=False,
        )
        log.info("Created dpevent")

        journal1 = dpevent["journal1"]
        _create_journalentries(journal1, 5)
        modified(journal1)

        journal2 = dpevent["journal2"]
        _create_journalentries(journal2, 15)
        modified(journal2)

        # add event with some content to archive
        dpevent_to_archive = api.content.create(
            container=event_config_folder,
            type="DPEvent",
            id="archived-event",
            title="Test Event that was archived",
            description="Die Beschreibung",
            EventType="Test",
            Status="inactive",
            AlertingStatus="none",
            AreaOfInterest="POLYGON((12.124842841725044 48.60077830054228,12.157801826095657 48.51533914735478,12.702998359223052 48.63164629148582,12.865046699043434 48.77393903963252,12.124842841725044 48.60077830054228))",
            EventCoordinates="POINT(12.240313700000002 48.59873489999998)",
            EventLocation=RelationValue(get_intid(dpnuclearpowerstation)),
            SectorizingNetworks=[RelationValue(get_intid(dpnetwork))],
            EventPhase=None,
            Exercise=True,
            TimeOfEvent=datetime.now(),
            OperationMode="routine",
            SectorizingSampleTypes=[
                "A",
                "A1",
                "A2",
                "A3",
            ],
            exclude_from_nav=False,
        )
        log.info("Created dpevent")

        journal1 = dpevent_to_archive["journal1"]
        _create_journalentries(journal1, 5)
        modified(journal1)

        journal2 = dpevent_to_archive["journal2"]
        _create_journalentries(journal2, 15)
        modified(journal2)

        # TODO:
        # Add SRModuleTypes
        # Add lagebericht-konfiguration
        # Add szenario
        # Add phase
        # Add modulkonfiguration

        with api.env.adopt_user(user=user1):
            # add one dpdocument for each type (except reireport)
            for doctype in doctypes:
                if doctype[0] in ["reireport", "doksysdokument"]:
                    # Do not create reireports here
                    continue
                new = api.content.create(
                    container=folder,
                    type="DPDocument",
                    title=f"Ein {doctype[1]}",
                    description=f"foo ({doctype[0]})",
                    docType=doctype[0],
                    text=RichTextValue(
                        f"<p>Text für {doctype[1]}</p>",
                        "text/html",
                        "text/x-html-safe",
                    ),
                    local_behaviors=["elan"],
                    scenarios=[dpevent.id],
                    exclude_from_nav=False,
                )
                api.content.create(
                    container=new,
                    type="Image",
                    title=f"{doctype[0]}_image",
                    image=dummy_image(),
                    exclude_from_nav=False,
                )
                try:
                    api.content.transition(obj=new, transition="publish")
                except Exception as e:
                    log.info(e)
                modified(new)
                log.info(f"Created dpdocument of type {doctype[0]}")

            # add full elan DPDocument
            new = api.content.create(
                container=folder,
                type="DPDocument",
                title="Eine Bodenprobe",
                description="foo",
                text=RichTextValue(
                    "<p>Bodenprobe!</p>", "text/html", "text/x-html-safe"
                ),
                docType="groundcontamination",
                scenarios=[dpevent.id],
                local_behaviors=["elan"],
                exclude_from_nav=False,
            )
            modified(new)
            api.content.create(
                container=new,
                type="Image",
                title="Ein Bild",
                image=dummy_image(),
                exclude_from_nav=False,
            )
            api.content.create(
                container=new,
                type="File",
                title="Eine Datei",
                file=dummy_file(),
                exclude_from_nav=False,
            )
            api.content.transition(obj=new, transition="publish")
            log.info(f"Created dpdocument Eine Bodenprobe {new.absolute_url()}")

            # add one full DPDocument to the event to archive
            new = api.content.create(
                container=folder,
                type="DPDocument",
                title="Eine ELAN Bodenprobe zum archivieren",
                description="foo",
                text=RichTextValue(
                    "<p>Bodenprobe!</p>", "text/html", "text/x-html-safe"
                ),
                docType="groundcontamination",
                scenarios=[dpevent_to_archive.id],
                local_behaviors=["elan"],
                exclude_from_nav=False,
            )
            modified(new)
            api.content.create(
                container=new,
                type="Image",
                title="Ein Bild",
                image=dummy_image(),
                exclude_from_nav=False,
            )
            api.content.create(
                container=new,
                type="File",
                title="Eine Datei",
                file=dummy_file(),
                exclude_from_nav=False,
            )
            api.content.transition(obj=new, transition="publish")
            log.info(f"Created dpdocument Eine Bodenprobe {new.absolute_url()}")

        # archive event
        dpevent_to_archive.archiveAndClose(self.request)

        # configure reireport (disable transfer)
        reireport_dtype = docpool_bund["config"]["dtypes"]["reireport"]
        from docpool.base.behaviors.transferstype import ITransfersType

        ITransfersType(reireport_dtype).allowTransfer = False

        # create REI Bericht
        folder = docpool_bund["content"]["Groups"]["bund_betreiber_he"]
        with api.env.adopt_user(username="betreiber_he"):
            new = api.content.create(
                container=folder,
                type="DPDocument",
                title="Ein Bericht",
                description="foo",
                text=RichTextValue(
                    "<p>Ein Bericht!</p>", "text/html", "text/x-html-safe"
                ),
                docType="reireport",
                local_behaviors=["rei"],
                Year=2017,
                Period="Q1",
                NuclearInstallations=["UCHL"],
                Medium="Fortluft",
                ReiLegalBases=["REI-E"],
                Origins=["unabhängige Messstelle"],
                MStIDs=["03132", "03141", "03151", "03161", "03171"],
                Authority="de_bw",
                PDFVersion="PDF/A-1b",
                exclude_from_nav=False,
            )
            new = api.content.create(
                container=folder,
                type="DPDocument",
                title="Ein Bericht",
                description="foo",
                text=RichTextValue(
                    "<p>Ein Bericht!</p>", "text/html", "text/x-html-safe"
                ),
                docType="reireport",
                local_behaviors=["rei"],
                Year=2020,
                Period="Q1",
                NuclearInstallations=["U07U"],
                Medium="Abwasser/Fortluft",
                ReiLegalBases=["REI-E"],
                Origins=["unabhängige Messstelle"],
                MStIDs=["03132", "03141", "03151", "03161", "03171"],
                Authority="de_bw",
                PDFVersion="PDF/A-1b",
                exclude_from_nav=False,
            )

        folder = docpool_bund["content"]["Groups"]["bund_aufsicht_by"]
        with api.env.adopt_user(username="aufsicht_by"):
            new = api.content.create(
                container=folder,
                type="DPDocument",
                title="Ein Bericht",
                description="foo",
                text=RichTextValue(
                    "<p>Ein Bericht!</p>", "text/html", "text/x-html-safe"
                ),
                docType="reireport",
                local_behaviors=["rei"],
                Year=2019,
                Period="M1",
                NuclearInstallations=["U13A"],
                Medium="",
                ReiLegalBases=["REI-I"],
                Origins=["Genehmigungsinhaber"],
                MStIDs=["09121"],
                Authority="de_mv",
                PDFVersion="PDF/A-1b",
                exclude_from_nav=False,
            )
            new = api.content.create(
                container=folder,
                type="DPDocument",
                title="Ein Bericht",
                description="foo",
                text=RichTextValue(
                    "<p>Ein Bericht!</p>", "text/html", "text/x-html-safe"
                ),
                docType="reireport",
                local_behaviors=["rei"],
                Year=2021,
                Period="M1",
                NuclearInstallations=["U07U"],
                Medium="Abwasser/Fortluft",
                ReiLegalBases=["REI-E"],
                Origins=["unabhängige Messstelle"],
                MStIDs=["03132", "03141", "03151", "03161", "03171"],
                Authority="de_bw",
                PDFVersion="PDF/A-1b",
                exclude_from_nav=False,
            )

        new = api.content.create(
            container=folder,
            type="DPDocument",
            title="Ein Bericht des Berichts",
            description="foo",
            text=RichTextValue("<p>Ein Bericht!</p>", "text/html", "text/x-html-safe"),
            docType="reireport",
            local_behaviors=["rei"],
            Year=2009,
            Period="M1",
            NuclearInstallations=["U08K"],
            Medium="Abwasser/Fortluft",
            ReiLegalBases=["REI-E"],
            Origins=["unabhängige Messstelle"],
            MStIDs=["03132", "03141", "03151", "03161", "03171"],
            Authority="de_bw",
            PDFVersion="PDF/A-1b",
            exclude_from_nav=False,
        )
        # Create Pinnwand Collections for Docpools
        dbconfig_bund = docpool_bund["contentconfig"]["dbconfig"]
        groundcontamination = docpool_bund["config"]["dtypes"]["groundcontamination"]
        pinnwand_bund = api.content.create(
            container=dbconfig_bund,
            type="DashboardCollection",
            id="pinnwand_bund",
            title="Default Bund Pinnwand",
            description="Default Bund Pinnwand",
            docTypes=[RelationValue(get_intid(groundcontamination))],
            exclude_from_nav=False,
        )
        # Set the create DCollection
        docpool_bund["esd"]["dashboard"].dbCollections = [
            RelationValue(get_intid(pinnwand_bund))
        ]

        # Add user to ContentSender & Reveivers
        api.group.add_user(groupname="bund_Senders", user=user1)
        api.group.add_user(groupname="hessen_Receivers", user=user2)

        # Add DPTransferFolder in hessen to receive data from bund
        dptranfers_folder = docpool_land["content"]["Transfers"]
        dptransferfolder = api.content.create(
            container=dptranfers_folder,
            type="DPTransferFolder",
            title="von Bund",
            description="foo",
            sendingESD=docpool_bund.UID(),
            permLevel="read/write",
            unknownDtDefault="block",
            unknownScenDefault="block",
            exclude_from_nav=False,
        )
        modified(dptransferfolder)

        # Create the same event in hessen as in bund to be able to transfer
        hessen_event = api.content.create(
            container=docpool_land["contentconfig"]["scen"],
            type="DPEvent",
            id="test-event",
            title="Test Event",
            description="Die Beschreibung",
            EventType="Exercise",
            Status="active",
            AlertingStatus="none",
            AreaOfInterest="POLYGON((12.124842841725044 48.60077830054228,12.157801826095657 48.51533914735478,12.702998359223052 48.63164629148582,12.865046699043434 48.77393903963252,12.124842841725044 48.60077830054228))",
            EventCoordinates="POINT(12.240313700000002 48.59873489999998)",
            EventPhase=None,
            Exercise=True,
            TimeOfEvent=datetime.now(),
            OperationMode="routine",
            SectorizingSampleTypes=[
                "A",
                "A1",
                "A2",
                "A3",
            ],
            exclude_from_nav=False,
        )
        log.info("Created test-event for hessen")

        from docpool.base.behaviors.transferable import ITransferable

        # transfer a elan document from bund to hessen
        doc_to_transfer = docpool_bund["content"]["Groups"]["bund_group1"][
            "eine-bodenprobe"
        ]
        adapted = ITransferable(doc_to_transfer)
        allowed = adapted.allowedTargets()
        target = allowed[0]
        adapted.transferToTargets(targets=[target])
        import_file_path = os.path.join(
            os.path.dirname(__file__), "../profiles/default/rei_search.xml"
        )
        # Configure EEA faceted navigation
        search = api.content.create(
            container=docpool_bund,
            type="Folder",
            id="rei-suche",
            title="Rei Suche",
            local_behaviors=["rei"],
            exclude_from_nav=False,
        )
        _configure_faceted_view(search, import_file_path, "faceted-table-items")
        return self.request.response.redirect(self.context.absolute_url())


def add_user(
    docpool,
    username,
    groupnames=None,
    enabled_apps=["elan", "doksys", "rei"],
):
    """Create a User and a Group for a docpool for testing.

    This mimicks adding groups in the application in docpool.users by:
    * adding the docpool-prefix to the groups id and title
    * allowing all doctypes
    * assigning the docpool

    """
    docpool_title = docpool.Title()
    prefix = docpool.prefix or docpool.id
    docpool_uid = IUUID(docpool)
    groupnames = groupnames if groupnames else []
    for groupname in groupnames:
        add_group(docpool, groupname)

    password = username
    password = f"dp_{username}"
    # add the user
    user_fullname = f"{username} ({docpool_title})"
    user = api.user.create(
        email="tester@plone.org",
        username=username,
        password=password,
        roles=("Member",),
        properties={"fullname": user_fullname},
    )
    user.setMemberProperties(
        {
            "fullname": user_fullname,
            "dp": docpool_uid,
            "apps": enabled_apps,
        }
    )
    # add the user to specified groups
    for groupname in groupnames:
        real_groupname = f"{prefix}_{groupname}"
        group = api.group.get(real_groupname)
        api.group.add_user(group=group, user=user)

    # Add the user to app-specific default-groups
    api.group.add_user(groupname=f"{prefix}_Members", user=user)
    if "doksys" in enabled_apps:
        api.group.add_user(groupname=f"{prefix}_DoksysUsers", user=user)
    if "elan" in enabled_apps:
        api.group.add_user(groupname=f"{prefix}_ELANUsers", user=user)
    if "rei" in enabled_apps:
        api.group.add_user(groupname=f"{prefix}_REIUsers", user=user)
    pm = getToolByName(docpool, "portal_membership")
    pm.createMemberArea(username)
    return user


def add_group(docpool, groupname):
    """Add a group in a docpool.

    This mimicks adding groups in the application by:
    * adding the docpool-prefix to the groups id and title
    * put all doctypes in memberdata to allow creating all DPDocuments
    * put docpool-id in memberdata
    """
    # get all doctypes to enable them for the new group
    voc = getUtility(IVocabularyFactory, name="docpool.base.vocabularies.DocType")
    doctypes = voc(docpool, raw=True)
    doctypes_ids = [i[0] for i in doctypes]
    # Do not create reireports. Can be added after creating the group.
    if "reireport" in doctypes_ids:
        doctypes_ids.remove("reireport")

    gtool = getToolByName(docpool, "portal_groups")
    docpool_uid = IUUID(docpool)
    docpool_title = docpool.Title()
    group_title = f"{groupname.capitalize()} ({docpool_title})"
    description = ""
    prefix = docpool.prefix or docpool.id
    groupname = f"{prefix}_{groupname}"

    if api.group.get(groupname=groupname) is not None:
        log.info(f"Skipping. Group {groupname} exists.")
        return

    props = {
        "title": group_title,
        "description": description,
        "dp": docpool_uid,
        "allowedDocTypes": doctypes_ids,
    }
    request = getRequest()
    if request.method != "POST":
        # fool addGroup to allow to work even without a real POST
        request.method = "POST"
    # this uses the monkey-patched addGroup from docpool.users
    # it will create a group-folder inside the docpool
    gtool.addGroup(
        id=groupname,
        roles=(),
        groups=(),
        properties=props,
        REQUEST=request,
        title=group_title,
        description=description,
    )
    return api.group.get(groupname)


def get_intid(obj):
    """Intid from intid-catalog"""
    intids = queryUtility(IIntIds)
    if intids is None:
        return
    # check that the object has an intid, otherwise there's nothing to be done
    try:
        return intids.getId(obj)
    except KeyError:  # noqa
        # The object has not been added to the ZODB yet
        return


def set_placeful_workflow(obj, workflow):
    if WorkflowPolicyConfig_id not in obj.keys():
        obj.manage_addProduct["CMFPlacefulWorkflow"].manage_addWorkflowPolicyConfig()
    wf_policy_config = getattr(obj, WorkflowPolicyConfig_id)
    wf_policy_config.setPolicyIn(workflow)
    wf_policy_config.setPolicyBelow(workflow)


def _configure_faceted_view(obj, config_file_name, layout_id):
    log.info(
        "Loading configuration {} for faceted view on {}".format(
            config_file_name, "/".join(obj.getPhysicalPath())
        )
    )
    subtyper = api.content.get_view("faceted_subtyper", obj, aq_get(obj, "REQUEST"))
    if not subtyper.is_faceted():
        subtyper.enable()
        import_file_path = os.path.join(
            os.path.dirname(__file__), "../profiles/default/", config_file_name
        )
        with open(import_file_path) as import_file:
            xml = import_file.read()
            environ = SnapshotImportContext(obj, "utf-8")
            importer = queryMultiAdapter((obj, environ), IBody)
            importer.body = xml
        obj.setLayout("facetednavigation_view")
        IAnnotations(obj)[ANNO_FACETED_LAYOUT] = layout_id
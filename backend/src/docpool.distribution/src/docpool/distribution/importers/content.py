from docpool.base.marker import IImportingMarker
from eea.facetednavigation.widgets.storage import Criterion
from elan.journal.adapters import JournalEntry
from persistent.list import PersistentList
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.dexterity.schema import SCHEMA_CACHE
from plone.dexterity.utils import resolveDottedName
from plone.exportimport.importers.content import ContentImporter
from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import WorkflowPolicyConfig_id
from zope.annotation.interfaces import IAnnotations
from zope.globalrequest import getRequest
from zope.interface import alsoProvides
from zope.interface import noLongerProvides


import dateutil
import logging

logger = logging.getLogger(__name__)


ANNOTATIONS_KEY = "exportimport.annotations"
MARKER_INTERFACES_KEY = "exportimport.marker_interfaces"

# Work around issues with fields based on Vocabularies
SIMPLE_SETTER_FIELDS = {
    "ALL": [],
    "CollaborationFolder": ["allowedDocTypes", "allowedPartnerDocTypes"],
    "DocType": ["automaticTransferTargets"],
    "DPDocument": ["scenarios", "OperationMode", "Origins"],
    "DPEvent": ["Status"],
    "DPTransferFolder": ["sendingESD"],
    "Folder": ["nextPreviousEnabled"],
    "GroupFolder": ["allowedDocTypes"],
    "SimpleFolder": ["allowedDocTypes"],
    "ReviewFolder": ["allowedDocTypes"],
}

FACTORY_KWARGS = {
    "ALL": ["supportedApps", "local_behaviors"],
    "DPDocument": ["docType"],
}


def global_obj_hook_before_deserializing(item, obj):
    """Hook to modify the created obj before deserializing the data."""
    # import simplesetter data before the rest
    for fieldname, value in item.get("exportimport.simplesetter", {}).items():
        setattr(obj, fieldname, value)

    for iface_name in item.pop(MARKER_INTERFACES_KEY, []):
        try:
            iface = resolveDottedName(iface_name)
            if not iface.providedBy(obj):
                alsoProvides(obj, iface)
                logger.info(
                    "Applied marker interface %s to %s",
                    iface_name,
                    obj.absolute_url(),
                )
        except ModuleNotFoundError:
            pass

    # Invalidate BehaviorAssignable cache for the obj
    # This is necessary so that the obj can be wrapped in the behavior interfaces
    request = getRequest()
    delattr(request, "__plone_dexterity_assignable_cache__")

    # Invalidate cache of provided interfaces
    # This is necessary so that the obj is correctly wrapped in the behavior interfaces
    # and thus fields can be found in the datamangers dm.set(value)
    try:
        delattr(obj, "_v__providedBy__")
    except AttributeError:
        pass

    SCHEMA_CACHE.clear()
    # this is not necessary
    # delattr(self.request, "__plone_dexterity_fti_cache__")
    return item, obj


def global_dict_hook(item, config):
    # Adapt this to your site
    old_portal_id = "dokpool"
    new_portal_id = "dokpool"

    if old_portal_id != new_portal_id:
        # This is only relevant for items in the site-root.
        # Most items containers are usually looked up by the uuid of the old parent
        item["@id"] = item["@id"].replace(f"/{old_portal_id}/", f"/{new_portal_id}/", 1)
        item["parent"]["@id"] = item["parent"]["@id"].replace(
            f"/{old_portal_id}", f"/{new_portal_id}", 1
        )

    # handle fields that should be set using a simple setter instead of a deserializer
    # this works around issues with validation
    simple = {}
    for fieldname in SIMPLE_SETTER_FIELDS.get("ALL", []):
        if fieldname in item:
            value = item.pop(fieldname)
            if value:
                simple[fieldname] = value
    for fieldname in SIMPLE_SETTER_FIELDS.get(item["@type"], []):
        if fieldname in item:
            value = item.pop(fieldname)
            if value:
                simple[fieldname] = value
    if simple:
        item["exportimport.simplesetter"] = simple

    # Add factory kwargs
    # these need to be set because subscribers to IObjectAddedEvent use it
    factory_kwargs = {}
    for fieldname in FACTORY_KWARGS.get("ALL", []):
        if fieldname in item:
            value = item.pop(fieldname)
            if value:
                factory_kwargs[fieldname] = value
    for fieldname in FACTORY_KWARGS.get(item["@type"], []):
        if fieldname in item:
            value = item.pop(fieldname)
            if value:
                factory_kwargs[fieldname] = value
    if factory_kwargs:
        item["factory_kwargs"] = factory_kwargs

    # Handle hidden required field in IREIDoc
    if "PDFVersion" in item and not item.get("PDFVersion"):
        item["PDFVersion"] = "keine Angabe"

    return item


def global_obj_hook(item, obj):
    SCHEMA_CACHE.clear()
    # Import Placeful Workflow
    # wf_policy = item.get("exportimport.workflow_policy")
    # if wf_policy:
    #     obj.manage_addProduct["CMFPlacefulWorkflow"].manage_addWorkflowPolicyConfig()
    #     wf_policy_config = obj[WorkflowPolicyConfig_id]
    #     wf_policy_config.setPolicyIn(
    #         wf_policy["workflow_policy_in"], update_security=True
    #     )
    #     wf_policy_config.setPolicyBelow(
    #         wf_policy["workflow_policy_below"], update_security=True
    #     )

    adapted = IExcludeFromNavigation(obj, None)
    if adapted is not None and adapted.exclude_from_nav is not True:
        adapted.exclude_from_nav = False
    item = import_annotations(obj, item)

    # Set mdate and wdate as a custom attribute
    # These are reused and dropped in ResetModifiedAndCreatedDate
    for attr in ["mdate", "wdate"]:
        value = item.get(attr, None)
        if value:
            value_as_date = dateutil.parser.parse(value)
            setattr(obj.aq_base, attr + "_migrated", value_as_date)
    for attr in ["created_by", "modified_by"]:
        value = item.get(attr, None)
        if value:
            setattr(obj.aq_base, attr + "_migrated", value)

    # Changelog is not imported because field is readonly
    if obj.portal_type == "DPEvent":
        if item.get("changelog"):
            obj.changelog = item["changelog"]
        if eventphase := item.get("exportimport.EventPhase", None):
            obj.EventPhase = eventphase

    if item.get("_last_journalentry_edition"):
        obj._last_journalentry_edition = item["_last_journalentry_edition"]

    if log := item.get("exportimport.transfer_receiver_log"):
        for entry in log:
            entry["timestamp"] = dateutil.parser.parse(entry["timestamp"])
        obj.transfer_receiver_log = log

    if log := item.get("exportimport.transfer_sender_log"):
        for entry in log:
            entry["timestamp"] = dateutil.parser.parse(entry["timestamp"])
        obj.transfer_sender_log = log

    return obj


class CustomContentImporter(ContentImporter):

    data_hooks = [global_dict_hook]
    pre_deserialize_hooks = [global_obj_hook_before_deserializing]
    obj_hooks = [global_obj_hook]

    def start(self):
        alsoProvides(self.request, IImportingMarker)

    def finish(self):
        noLongerProvides(self.request, IImportingMarker)


def import_annotations(obj, item):
    annotations = IAnnotations(obj)
    for key in item.get(ANNOTATIONS_KEY, []):
        if key == "journal.journalentries":
            # handle JournalEntry
            if not item[ANNOTATIONS_KEY]["journal.journalentries"]:
                continue
            entries = PersistentList()
            for data in item[ANNOTATIONS_KEY]["journal.journalentries"]:
                if not data:
                    continue
                entry = JournalEntry(title=data["title"], text=data["text"])
                entry.creator = data["creator"]
                entry.created = dateutil.parser.parse(data["created"])
                entry.modified = dateutil.parser.parse(data["modified"])
                entry.timestamp = data["timestamp"]
                entries.append(entry)
            if entries:
                annotations[key] = entries
        elif key == "FacetedCriteria":
            if not item[ANNOTATIONS_KEY]["FacetedCriteria"]:
                continue
            entries = PersistentList()
            for data in item[ANNOTATIONS_KEY]["FacetedCriteria"]:
                if not data:
                    continue
                data["_cid_"] = data.pop("__name__")
                entry = Criterion(**data)
                entries.append(entry)
            if entries:
                annotations[key] = entries
        else:
            annotations[key] = item[ANNOTATIONS_KEY][key]
    return item

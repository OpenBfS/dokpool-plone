from plone.exportimport.exporters.content import ContentExporter
from plone.restapi.interfaces import IJsonCompatible
from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import WorkflowPolicyConfig_id
from zope.annotation.interfaces import IAnnotations
from zope.globalrequest import getRequest
from zope.interface import directlyProvidedBy


IGNORED_TYPES = [
    "Discussion Item",
    "TempFolder",
]

MARKER_INTERFACES_TO_EXPORT = [
    "eea.facetednavigation.interfaces.IFacetedNavigable",
    "eea.facetednavigation.subtypes.interfaces.IFacetedNavigable",
    "eea.facetednavigation.settings.interfaces.IDisableSmartFacets",
    "eea.facetednavigation.settings.interfaces.IHidePloneLeftColumn",
    "eea.facetednavigation.settings.interfaces.IHidePloneRightColumn",
    "docpool.base.events.IDocumentPoolUndeleteable",
]

ANNOTATIONS_TO_EXPORT = [
    "journal.journalentries",
    "FacetedCriteria",
    "FacetedLayout",
    "FacetedVersion",
    "docpool_applications_key",
]

ANNOTATIONS_KEY = "exportimport.annotations"

MARKER_INTERFACES_KEY = "exportimport.marker_interfaces"


def global_obj_hook(obj, config):
    """Used this to inspect the content item before serialisation data.
    Bad: Changing the content-item is a bad idea.
    Good: Return None if you want to skip this particular object.
    """
    request = getRequest()
    if obj.portal_type in IGNORED_TYPES:
        return

    # Reset custom behavior cache to prevent exporting data from
    # local_behaviors that are not enabled!
    if request.other.get("savedLocalBehaviors") is not None:
        request.other.pop("savedLocalBehaviors", None)
    return obj


def global_dict_hook(item, obj, config):
    """Used this to modify the serialized data.
    Return None if you want to skip this particular object.
    """
    # remove site root
    if item["@type"] == "Plone Site":
        # To avoid a conflict between @id and id
        item["@id"] = f"/{item['id']}"

    if not item.get("creators") and obj.aq_base.creators:
        item["creators"] = IJsonCompatible(obj.creators, obj)

    if obj.isPrincipiaFolderish and WorkflowPolicyConfig_id in obj.keys():
        wf_policy = obj[WorkflowPolicyConfig_id]
        item["exportimport.workflow_policy"] = {
            "workflow_policy_below": wf_policy.workflow_policy_below,
            "workflow_policy_in": wf_policy.workflow_policy_in,
        }

    if log := getattr(obj.aq_base, "transfer_receiver_log", None):
        item["exportimport.transfer_receiver_log"] = IJsonCompatible(log, obj)

    if log := getattr(obj.aq_base, "transfer_sender_log", None):
        item["exportimport.transfer_sender_log"] = IJsonCompatible(log, obj)

    item = export_marker_interfaces(item, obj)
    item = export_annotations(item, obj)

    # drop versioning data
    item.pop("versioning_enabled", None)
    item.pop("exportimport.versions", None)
    item.pop("changeActor", None)
    item.pop("changeNote", None)

    return item


def dict_hook_dpevent(item, obj, config):
    """Used this to modify the serialized data.
    Return None if you want to skip this particular object.
    """
    if obj.portal_type.lower() != "dpevent":
        return item
    if obj.EventPhase:
        item["exportimport.EventPhase"] = obj.EventPhase.to_object.title
    return item


def export_annotations(item, obj):
    results = {}
    annotations = IAnnotations(obj)
    for key in ANNOTATIONS_TO_EXPORT:
        data = annotations.get(key)
        if data:
            results[key] = IJsonCompatible(data, None)
    if results:
        item[ANNOTATIONS_KEY] = results
    return item


def export_marker_interfaces(item, obj):
    interfaces = [i.__identifier__ for i in directlyProvidedBy(obj)]
    interfaces = [i for i in interfaces if i in MARKER_INTERFACES_TO_EXPORT]
    if interfaces:
        item[MARKER_INTERFACES_KEY] = interfaces
    return item


class CustomContentExporter(ContentExporter):
    obj_hooks = [global_obj_hook]
    data_hooks = [
        global_dict_hook,
        dict_hook_dpevent,
    ]

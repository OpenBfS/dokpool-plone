from docpool.base.content.doctype import DocType
from docpool.base.content.dptransferfolder import IDPTransferFolder
from operator import itemgetter
from plone import api


def allowed_targets(context):
    """
    Other ESD must have allowed communication with my ESD,
    my DocType is known and must be accepted
        or the DocType is not defined in the other ESD (will be checked later)
        or we don't even have a DocType (because, e.g., we're about to create one)
    and, if context is a document,
        my current version must not have been transferred.
    """
    from docpool.base.behaviors.transferable import ITransferable

    try:
        esd = context.myDocumentPool()
    except AttributeError:
        return []

    if isinstance(context, DocType):
        dto = context
    else:
        try:
            dto_ = context.docTypeObj
        except AttributeError:
            dto = None
        else:
            dto = dto_()
    dt_id = dto.id if dto else "---"

    targets = []
    portal_catalog = api.portal.get_tool("portal_catalog")

    # ContentSenders do not need access to the target folders!
    for brain in portal_catalog.unrestrictedSearchResults(
        object_provides=IDPTransferFolder.__identifier__, sendingESD=esd.UID()
    ):
        obj = brain._unrestrictedGetObject()
        permission = obj.doctype_permission(dt_id)
        if permission != "block":
            from_to_title = obj.from_to_title()
            target_docpool = obj.myDocumentPool()
            targets.append({"uid": brain.UID, "from_to_title": from_to_title, "target_apps": target_docpool.supportedApps})

    transferable = ITransferable(context, None)
    if transferable is not None:
        mdate = context.getMdate()
        sent_to_since_last_modified = {
            entry["transferfolder_uid"] for entry in transferable.sender_log if entry["timestamp"] > mdate
        }
        targets = [t for t in targets if t["uid"] not in sent_to_since_last_modified]

    return sorted(targets, key=itemgetter("from_to_title"))

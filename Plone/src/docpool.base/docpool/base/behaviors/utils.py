from docpool.base.content.doctype import DocType
from docpool.base.content.dptransferfolder import IDPTransferFolder
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

    brains = api.content.find(object_provides=IDPTransferFolder, sendingESD=esd.UID())

    dt_perm = lambda brain: brain.getObject().doctypePermissions.get(dt_id, False)
    targets = [
        brain.UID for brain in brains if not (perm := dt_perm(brain)) or perm != "block"
    ]

    transferable = ITransferable(context, None)
    if transferable is not None:
        mdate = context.getMdate()
        sent_to_since_last_modified = {
            entry["transferfolder_uid"]
            for entry in transferable.sender_log
            if entry["timestamp"] > mdate
        }
        targets = [t for t in targets if t not in sent_to_since_last_modified]

    return targets

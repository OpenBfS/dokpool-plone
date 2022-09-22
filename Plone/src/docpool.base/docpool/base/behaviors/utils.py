from docpool.base.behaviors.transferable import ITransferable
from docpool.base.content.doctype import DocType
from docpool.base.content.dpdocument import DPDocument
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
    adapted = ITransferable(context, None)
    if not adapted:
        return []
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

    if isinstance(context, DPDocument):
        mdate = context.getMdate()
        sent_to_since_last_modified = {
            entry["transferfolder_uid"]
            for entry in adapted.sender_log
            if entry["timestamp"] > mdate
        }
        targets = [t for t in targets if t not in sent_to_since_last_modified]

    return targets

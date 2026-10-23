from docpool.base.content.doctype import DocType
from docpool.base.content.dptransferfolder import IDPTransferFolder
from docpool.base.content.places import IPlaces
from plone import api


def allowed_targets(context):
    """
    Other ESD must have allowed communication with my ESD,
    my DocType is known and must be accepted
        or the DocType is not defined in the other ESD (will be checked later)
        or we don't even have a DocType (because, e.g., we're about to create one)
    and context must not have been transferred.
    """
    from docpool.base.behaviors.transferable import ITransferable

    try:
        esd = IPlaces(context).document_pool
    except AttributeError:
        return []

    if not esd:
        # We're not inside a docpool
        return []

    if isinstance(context, DocType):
        dt_id = context.id
    else:
        try:
            doctype_data = context.doctype_data()
        except AttributeError:
            doctype_data = {}
        dt_id = doctype_data.get("id", "---")

    targets = [
        obj
        for brain in api.content.find(
            object_provides=IDPTransferFolder.__identifier__,
            sendingESD=esd.UID(),
            unrestricted=True,  # ContentSenders do not need access to the target folders!
        )
        if (obj := brain._unrestrictedGetObject()).acceptsDT(dt_id)
    ]

    transferable = ITransferable(context, None)
    if transferable is not None:
        sent_to = {entry["transferfolder_uid"] for entry in transferable.sender_log}
        targets = [t for t in targets if t.UID() not in sent_to]

    return targets

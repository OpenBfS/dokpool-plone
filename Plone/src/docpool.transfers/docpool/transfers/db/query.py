from docpool.base.content.doctype import DocType
from docpool.base.content.dpdocument import DPDocument
from docpool.dbaccess.dbinit import __session__
from docpool.transfers.db.model import Channel
from plone import api
from sqlalchemy import and_


def allowed_targets(context):
    """
    Other ESD must have allowed communication with my ESD,
    my DocType is known and must be accepted
        or the DocType is not defined in the other ESD (will be checked later)
        or we don't even have a DocType (because, e.g., we're about to create one)
    and, if context is a document,
        my current version must not have been transferred.
    """
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
    dt_id = dto.id if dto else '---'

    filter_list = (
        Channel.esd_from_uid == esd.UID(),
    )
    q = (
        __session__.query(Channel)
        .filter(and_(*filter_list))
        .order_by('esd_from_title')
    )
    targets = q.all()

    tf = lambda t: api.content.get(UID=t.tf_uid)
    targets = [
        t
        for t in targets
        if not (perm := tf(t).doctypePermissions.get(dt_id, False)) or perm != 'block'
    ]

    if isinstance(context, DPDocument):
        mdate = context.getMdate()
        sent_to_since_last_modified = set(
            entry['transferfolder_uid']
            for entry in context.sender_log
            if entry['timestamp'] > mdate
        )
        targets = [t for t in targets if t.tf_uid not in sent_to_since_last_modified]

    return targets

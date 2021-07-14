from docpool.base.content.doctype import DocType
from docpool.dbaccess.dbinit import __session__
from docpool.transfers.db.model import Channel
from docpool.transfers.db.model import DocTypePermission
from docpool.transfers.db.model import SenderLog
from sqlalchemy import and_
from sqlalchemy import or_


def allowed_targets(context):
    """
    Other ESD must have allowed communication with my ESD,
    my DocType is known and must be accepted
        or the DocType is not defined in the other ESD (will be checked later)
    and, if context is a document,
        my current version must not have been transferred.
    """
    try:
        esd = context.myDocumentPool()
    except AttributeError:
        return []

    dto = context if isinstance(context, DocType) else context.docTypeObj()
    dt_id = dto.id if dto else '---'
    filter_list = (
        Channel.esd_from_uid == esd.UID(),
        or_(
            and_(
                DocTypePermission.doc_type == dt_id,
                DocTypePermission.perm != 'block',
            ),
            ~Channel.permissions.any(
                DocTypePermission.doc_type == dt_id),
        ),
    )
    if isinstance(context, DPDocument):
        filter_list += (
            ~Channel.sends.any(
                and_(
                    SenderLog.document_uid == context.UID(),
                    SenderLog.timestamp > context.getMdate(),
                )
            ),
        )
    q = (
        __session__.query(Channel)
        .outerjoin(Channel.permissions)
        .outerjoin(Channel.sends)
        .filter(and_(*filter_list))
        .order_by('esd_from_title')
    )
    targets = q.all()
    return targets

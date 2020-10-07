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
    and my current version must not have been transferred.
    """
    esd_uid = context.myDocumentPool().UID()
    # print esd_uid
    dto = context.docTypeObj()
    dt_id = dto and dto.id or '---'
    # print dt_id
    m = context.getMdate()
    # print m
    q = (
        __session__.query(Channel)
        .outerjoin(Channel.permissions)
        .outerjoin(Channel.sends)
        .filter(
            and_(
                Channel.esd_from_uid == esd_uid,
                or_(
                    and_(
                        DocTypePermission.doc_type == dt_id,
                        DocTypePermission.perm != 'block',
                    ),
                    ~Channel.permissions.any(
                        DocTypePermission.doc_type == dt_id),
                ),
                ~Channel.sends.any(
                    and_(
                        SenderLog.document_uid == context.UID(),
                        SenderLog.timestamp > m,
                    )
                ),
            )
        )
        .order_by('esd_from_title')
    )
    # print q.statement
    targets = q.all()
    # print len(targets)
    return targets

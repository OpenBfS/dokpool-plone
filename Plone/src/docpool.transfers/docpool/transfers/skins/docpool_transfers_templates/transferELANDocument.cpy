from Products.CMFPlone import MessageFactory
_ = MessageFactory('elan.esd')
from Products.CMFPlone.utils import log, log_exc

request = context.REQUEST
elandocid = request.get('elandocid')
targetIds = request.get("targets")


if targetIds:
    try:
        doc, elandoc = context.getTupleForTransfer(id=elandocid)
        elandoc.manage_transfer(targetIds)
        log("Transfer %s to ChannelIDs: %s" % (doc.Title(), targetIds))
        return _("Transfer executed")
    except Exception, e:
        log_exc(e)
        return _("Transfer error: ") + str(e)
  
#state.setNextAction('redirect_to:python:object.absolute_url()')
#return state

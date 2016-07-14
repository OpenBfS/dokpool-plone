from Products.CMFPlone import MessageFactory
_ = MessageFactory('docpool.transfers')
from Products.CMFPlone.utils import log, log_exc

request = context.REQUEST
dpdocid = request.get('dpdocid')
targetIds = request.get("targets")


if targetIds:
    try:
        doc, dpdoc = context.getTupleForTransfer(id=dpdocid)
        dpdoc.manage_transfer(targetIds)
        log("Transfer %s to ChannelIDs: %s" % (doc.Title(), targetIds))
        return _("Transfer executed")
    except Exception, e:
        log_exc(e)
        return _("Transfer error: ") + str(e)
  
#state.setNextAction('redirect_to:python:object.absolute_url()')
#return state

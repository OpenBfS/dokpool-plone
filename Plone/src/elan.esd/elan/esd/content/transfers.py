# -*- coding: utf-8 -*-
from docpool.base.utils import queryForObject, _copyPaste
from docpool.elan.config import ELAN_APP
from elan.esd.db.model import Channel, ChannelPermissions
from elan.dbaccess.dbinit import __session__
from Products.CMFCore.utils import getToolByName
from plone import api
from elan.esd.behaviors.elandoctype import IELANDocType

def determineChannels(transfer_ids):
    channels = __session__.query(Channel).filter(Channel.id.in_(transfer_ids)).all()
    return channels

def determineTransferFolderObject(self, channel):
    uid = channel.tf_uid
    return queryForObject(self, UID=uid)

def ensureDocTypeInTarget(original, copy):
    my_dt = original.docType
    config = copy.myDocumentPool().config.dtypes
    if config.hasObject(my_dt):
        return
    dtObj = original.docTypeObj()
    id = _copyPaste(dtObj,config)
    new_dt = config._getOb(id)
    new_dt.extension(ELAN_APP).setCCategory('recent') # Set intermediate category
    wftool = getToolByName(original, 'portal_workflow')
    wftool.doActionFor(new_dt, 'retract')
    new_dt.reindexObject()
    new_dt.reindexObjectSecurity()
    config.reindexObject()
    
def ensureScenariosInTarget(original, copy):
    my_scenarios = original.extension(ELAN_APP).scenarios
    scen_source = original.myDocumentPool().contentconfig.scen
    scen = copy.myDocumentPool().contentconfig.scen
    new_scenarios = []
    wftool = getToolByName(original, 'portal_workflow')
    for scenario in my_scenarios:
        if scen.hasObject(scenario):
            s = scen._getOb(scenario)
            if wftool.getInfoFor(s, 'review_state') == 'private':
                sscen = s.substitute and s.substitute.to_object or None
                if sscen and sscen.canBeAssigned():
                    substitute = sscen.getId()
                    new_scenarios.append(substitute)
                else:
                    new_scenarios.append(scenario)
            else:
                new_scenarios.append(scenario)
        else:
            s = scen_source._getOb(scenario)
            id = _copyPaste(s,scen)
            new_scen = scen._getOb(id)
            wftool = getToolByName(original, 'portal_workflow')
            wftool.doActionFor(new_scen, 'retract')
            new_scenarios.append(id)
    copy.extension(ELAN_APP).scenarios = new_scenarios
    copy.reindexObject()


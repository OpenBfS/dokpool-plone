# -*- coding: utf-8 -*-
from docpool.config.local import createELANStructure, createTransferArea,\
    createELANUsers, createELANGroups, setELANLocalRoles
from docpool.config.general import connectTypesAndCategories


def esdAdded(obj, event=None):
    """
    """
    self = obj
    createELANStructure(self, True)
    createTransferArea(self, True)
    connectTypesAndCategories(self)
    createELANUsers(self)
    createELANGroups(self)
    setELANLocalRoles(self)
    self.reindexAll()

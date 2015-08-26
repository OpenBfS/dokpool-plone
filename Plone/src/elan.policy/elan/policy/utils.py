# -*- coding: utf-8 -*-

from docpool.config.general import configureFiltering, configUserFolders,\
    createStructure, navSettings, setFrontpage, createGroups,\
    connectTypesAndCategories

def install(self):
    """
    """
    fresh = True
    if self.hasObject("config"):
        fresh = False # It's a reinstall
    configUserFolders(self, fresh)
    createStructure(self, fresh)
    navSettings(self)
    if fresh:
        connectTypesAndCategories(self)
    createGroups(self)
    configureFiltering(self)
    setFrontpage(self)
    


    

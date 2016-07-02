# -*- coding: utf-8 -*-

APP_REGISTRY = {}

def registerApp(name, typeFactoryMethod, documentFactoryMethod, dpAddedMethod, dpRemovedMethod):
    """
    @param name:
    @param factoryMethod:
    @return:
    """
    APP_REGISTRY[name] = { 'typeFactoryMethod' : typeFactoryMethod,
                           'documentFactoryMethod' : documentFactoryMethod,
                           'dpAddedMethod': dpAddedMethod,
                           'dpRemovedMethod': dpRemovedMethod}

def createTypeObject(name, self):
    APP_REGISTRY[name]['typeFactoryMethod'](self)
    return self._getOb(name)

def createDocumentObject(name, self):
    APP_REGISTRY[name]['documentFactoryMethod'](self)
    return self._getOb(name)

def activeApps():
    apps = APP_REGISTRY.keys()
    apps.sort()
    return apps
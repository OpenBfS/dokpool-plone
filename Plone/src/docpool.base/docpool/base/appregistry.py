# -*- coding: utf-8 -*-

APP_REGISTRY = {}

def registerApp(name, title, typeFactoryMethod, documentFactoryMethod, dpAddedMethod, dpRemovedMethod):
    """
    @param name:
    @param factoryMethod:
    @return:
    """
    APP_REGISTRY[name] = {  'title' : title,
                            'typeFactoryMethod' : typeFactoryMethod,
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
    """
    Return all active applications.
    @return:
    """
    apps = APP_REGISTRY.keys()
    apps.sort()
    return [ ( appname, APP_REGISTRY[appname]['title']) for appname in apps ]

def extendingApps():
    """
    Just those apps, that actually provide dynamic extensions to documents.
    @return:
    """
    apps = APP_REGISTRY.keys()
    apps.sort()
    return [ ( appname, APP_REGISTRY[appname]['title']) for appname in apps if APP_REGISTRY[appname].get('documentFactoryMethod', None) ]
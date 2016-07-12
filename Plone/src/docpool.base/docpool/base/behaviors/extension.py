# -*- coding: utf-8 -*-
from zope.component import getMultiAdapter
from zope.interface import implements
from docpool.base.interfaces import IApplicationAware

class Extension(object):
    implements(IApplicationAware)

    def docTypeObj(self):
        return None

    def getPortalTypeName(self):
        return self.__class__.__name__

    def extView(self, name, request):
        return getMultiAdapter((self, request), name=name)



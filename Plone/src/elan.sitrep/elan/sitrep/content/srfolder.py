#
# File: srfolder.py
#
# Copyright (c) 2017 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the SRFolder content type. See srfolder.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.base.content.simplefolder import ISimpleFolder
from docpool.base.content.simplefolder import SimpleFolder
from docpool.elan.config import ELAN_APP
from elan.sitrep.vocabularies import ModuleTypesVocabularyFactory
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class ISRFolder(model.Schema, ISimpleFolder):
    """
    """

    directives.omitted('allowedDocTypes')


@implementer(ISRFolder)
class SRFolder(Container, SimpleFolder):
    """
    """

    security = ClassSecurityInfo()

    APP = ELAN_APP

    def modTypes(self):
        """
        """
        return ModuleTypesVocabularyFactory(self, raw=True)

    def customMenu(self, menu_items):
        """
        """
        res = []
        for menu_item in menu_items:
            if menu_item.get('id') == 'SRModule':
                for mt in self.modTypes():
                    res.append(
                        {
                            'extra': {
                                'separator': None,
                                'id': mt[0],
                                'class': 'contenttype-%s' % mt[0],
                            },
                            'submenu': None,
                            'description': '',
                            'title': mt[1],
                            'action': '%s/++add++SRModule?form.widgets.docType:list=%s'
                            % (self.absolute_url(), mt[0]),
                            'selected': False,
                            'id': mt[0],
                            'icon': None,
                        }
                    )
            else:
                res.append(menu_item)
        return res

    def mySRFolder(self):
        """
        """
        return self

    def getFirstChild(self):
        """
        """
        fc = self.getFolderContents()
        if len(fc) > 0:
            return fc[0].getObject()
        else:
            return None

    def getAllContentObjects(self):
        """
        """
        return [obj.getObject() for obj in self.getFolderContents()]

    def getSRFolders(self, **kwargs):
        """
        """
        args = {'portal_type': 'SRFolder'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getSRModules(self, **kwargs):
        """
        """
        args = {'portal_type': 'SRModule'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getSituationReports(self, **kwargs):
        """
        """
        args = {'portal_type': 'SituationReport'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

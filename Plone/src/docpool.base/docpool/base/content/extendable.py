#
# File: extendable.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the Extendable content type. See extendable.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.base.appregistry import APP_REGISTRY
from docpool.base.appregistry import appIcon
from docpool.base.utils import getActiveAllowedPersonalBehaviorsForDocument
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer


class IExtendable(model.Schema):
    """
    """


@implementer(IExtendable)
class Extendable(Item):
    """
    """

    security = ClassSecurityInfo()

    def doc_extension(self, applicationName):
        """
        Get the object for the extension related to the given application.
        @param applicationName: the name of the application
        @return: the extension object
        """
        return APP_REGISTRY[applicationName]['documentBehavior'](
            self
        )  # and APP_REGISTRY[applicationName]['documentBehavior'](self) or self

    def type_extension(self, applicationName):
        return APP_REGISTRY[applicationName]['typeBehavior'](
            self
        )  # and APP_REGISTRY[applicationName]['typeBehavior'](self) or self

    def myExtensionIcons(self, request):
        """

        @param request:
        @return:
        """
        behaviorNames = getActiveAllowedPersonalBehaviorsForDocument(
            self, request)
        if behaviorNames:
            return [appIcon(name) for name in behaviorNames if appIcon(name)]
        else:
            return []

    # FIXME: potential performance leak
    def myExtensions(self, request):
        """

        @return:
        """
        behaviorNames = getActiveAllowedPersonalBehaviorsForDocument(
            self, request)
        # print "myExtensions", behaviorNames
        return [self.doc_extension(name) for name in behaviorNames]

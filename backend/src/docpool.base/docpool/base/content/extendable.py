from AccessControl import ClassSecurityInfo
from docpool.base.appregistry import APP_REGISTRY
from docpool.base.appregistry import appIcon
from docpool.base.utils import getActiveAllowedPersonalBehaviorsForDocument


class Extendable:
    """Mixin class used by DPDocument and DocType."""

    def doc_extension(self, applicationName):
        """
        Get the object for the extension related to the given application.
        @param applicationName: the name of the application
        @return: the extension object
        """
        return APP_REGISTRY[applicationName]["documentBehavior"](
            self
        )  # and APP_REGISTRY[applicationName]['documentBehavior'](self) or self

    def type_extension(self, applicationName):
        return APP_REGISTRY[applicationName]["typeBehavior"](
            self
        )  # and APP_REGISTRY[applicationName]['typeBehavior'](self) or self

    def myExtensionIcons(self, request):
        """

        @param request:
        @return:
        """
        behaviorNames = getActiveAllowedPersonalBehaviorsForDocument(self, request)
        if behaviorNames:
            return [appIcon(name) for name in behaviorNames if appIcon(name)]
        else:
            return []

    # FIXME: potential performance leak
    def myExtensions(self, request):
        """

        @return:
        """
        behaviorNames = getActiveAllowedPersonalBehaviorsForDocument(self, request)
        # print "myExtensions", behaviorNames
        return [self.doc_extension(name) for name in behaviorNames]

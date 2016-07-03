# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from plone.memoize.view import memoize
from docpool.base.appregistry import extendingApps
class ApplicationState(BrowserView):
    """
    This provides access to information related to the current (user-specific) state.
    """

    @memoize
    def appsAvailableToCurrentUser(self):
        """

        @return:
        """
        return [app[0] for app in extendingApps()]

    @memoize
    def appsActivatedByCurrentUser(self):
        """

        @return:
        """
        #return [ 'transfers' ]
        return [app[0] for app in extendingApps()]

    @memoize
    def effectiveAppsHere(self):
        """

        @return:
        """
        return tuple(set(self.appsActivatedByCurrentUser()).intersection(set(self.appsSupportedHere())))

    @memoize
    def appsSupportedHere(self):
        """

        @return:
        """
        return self.context.allSupportedApps()

    @memoize
    def isCurrentlyActive(self, appname):
        """
        @param appname:
        @return:
        """
        return appname in self.effectiveAppsHere()
# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from plone.memoize.view import memoize
from docpool.base.appregistry import extendingApps, implicitApps
from plone import api
from docpool.localbehavior.localbehavior import ILocalBehaviorSupport


class ApplicationState(BrowserView):
    """
    This provides access to information related to the current (user-specific) state.
    """

    def appsPermittedForObject(self, request):

        available_apps = self.appsAvailableToCurrentUser()
        # Now get the type.
        if hasattr(self.context, "docTypeObj"):
            dto = self.context.docTypeObj()
        else:
            dt = request.get('docType', '')
            if dt:
                try:
                    dto = self.context.config.dtypes[dt]
                except Exception, e:
                    pass
        if dto:
            supportedByType = ILocalBehaviorSupport(dto).local_behaviors
            print "supportedByType ", supportedByType
            available_apps = list(set(available_apps).intersection(supportedByType))
        available_apps.extend([ app[0] for app in implicitApps()])
        print "appsPermittedForObject ", available_apps, self.locallyAcivated()
        return available_apps

    def appsEffectiveForObject(self, request, filtered=False):
        effective = self.appsPermittedForObject(request)
        if filtered:
            effective = list(set(effective).intersection(self.appsActivatedByCurrentUser()))
            effective.extend([app[0] for app in implicitApps()])
        effective = list(set(effective).intersection(self.locallyAcivated()))
        print "appsEffectiveForObject ", effective
        return effective

    @memoize
    def locallyAcivated(self):
        res = getattr(self.context, 'local_behaviors', [])
        res.extend([ app[0] for app in implicitApps()])
        return res

    @memoize
    def appsPermittedForCurrentUser(self):
        """

        @return:
        """
        roles = api.user.get_roles(obj=self.context)
        # Administrators have every application right
        if "Manager" in roles or "Site Administrator" in roles:
            return [app[0] for app in extendingApps()]

        # Others have explicit roles
        res = []
        for role in roles:
            # All application roles end with "User"
            if role.endswith("User"):
                res.append(role[:-len("User")].lower())
        #print "local roles: ", res
        return res

    @memoize
    def appsAvailableToCurrentUser(self):
        """

        @return:
        """
        return list(set(self.appsPermittedForCurrentUser()).intersection(set(self.appsSupportedHere())))

    def appsActivatedByCurrentUser(self):
        """

        @return:
        """
        user = api.user.get_current()
        if user.getUserName() == 'admin':
            return [app[0] for app in extendingApps() ]
        res = user.getProperty("apps", default=[])
        print "appsActivatedByCurrentUser: ", res
        return res

    @memoize
    def effectiveAppsHere(self):
        """
        @return:
        """
        return list(set(self.appsActivatedByCurrentUser()).intersection(set(self.appsSupportedHere())))

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
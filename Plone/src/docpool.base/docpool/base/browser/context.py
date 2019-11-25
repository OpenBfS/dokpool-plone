# -*- coding: utf-8 -*-
from docpool.base.appregistry import extendingApps
from docpool.base.appregistry import implicitApps
from docpool.base.config import BASE_APP
from docpool.localbehavior.localbehavior import ILocalBehaviorSupport
from plone import api
from plone.memoize.view import memoize
from Products.Five import BrowserView


class ApplicationState(BrowserView):
    """
    This provides access to information related to the current (user-specific) state.
    """

    def appsPermittedForObject(self, request):

        available_apps = self.appsAvailableToCurrentUser()
        # Now get the type.
        dto = None
        if hasattr(self.context, "docTypeObj"):
            dto = self.context.docTypeObj()
        else:
            dtFromRequest = request.get('form.widgets.docType', [''])
            if isinstance(dtFromRequest, type('')):
                dtFromRequest = [dtFromRequest]
            dt = request.get('docType', dtFromRequest[0])
            if dt:
                try:
                    dto = self.context.config.dtypes[dt]
                except Exception as e:
                    # print "no doctype %s available to check specific app support" % dt
                    pass

        if dto:
            try:
                supportedByType = ILocalBehaviorSupport(dto).local_behaviors
                # print "supportedByType ", supportedByType
                available_apps = list(
                    set(available_apps).intersection(supportedByType))
            # Type may not support local behavior (e.g. SR module types)
            except BaseException:
                pass
        available_apps.extend([app[0] for app in implicitApps()])
        # print "appsPermittedForObject ", available_apps, self.locallyAcivated()
        return list(set(available_apps))

    def appsEffectiveForObject(self, request, filtered=False):
        effective = self.appsPermittedForObject(request)
        # print "permitted", effective
        if filtered:
            # print "activated", self.appsActivatedByCurrentUser()
            effective = list(
                set(effective).intersection(self.appsActivatedByCurrentUser())
            )
            effective.extend([app[0] for app in implicitApps()])
        # print "locallyActivated", self.locallyAcivated()
        effective = list(set(effective).intersection(self.locallyAcivated()))
        # print "appsEffectiveForObject ", effective
        return list(set(effective))

    def locallyAcivated(self):
        res = getattr(self.context, 'local_behaviors', [])[:]
        res.extend([app[0] for app in implicitApps()])
        return list(set(res))

    @memoize
    def appsPermittedForCurrentUser(self):
        """

        @return:
        """
        roles = []
        try:
            roles = api.user.get_roles(obj=self.context)
            # Administrators have every application right
            if "Manager" in roles or "Site Administrator" in roles:
                return [app[0] for app in extendingApps()]
        except BaseException:
            pass
        # Others have explicit roles
        res = []
        for role in roles:
            # All application roles end with "User"
            if role.endswith("User"):
                res.append(role[: -len("User")].lower())
        # print "local roles: ", res

        return list(set(res))

    @memoize
    def appsAvailableToCurrentUser(self):
        """

        @return:
        """
        return list(
            set(self.appsPermittedForCurrentUser()).intersection(
                set(self.appsSupportedHere())
            )
        )

    def appsActivatedByCurrentUser(self):
        """

        @return:
        """
        user = api.user.get_current()
        res = user.getProperty("apps") or [BASE_APP]
        # print "appsActivatedByCurrentUser: ", res
        return list(set(res))

    @memoize
    def effectiveAppsHere(self):
        """
        @return:
        """
        return list(
            set(self.appsActivatedByCurrentUser()).intersection(
                set(self.appsSupportedHere())
            )
        )

    @memoize
    def appsSupportedHere(self):
        """

        @return:
        """
        try:
            return list(set(self.context.allSupportedApps()))
        except BaseException:
            return []

    @memoize
    def isCurrentlyActive(self, appname):
        """
        @param appname:
        @return:
        """
        return appname in self.effectiveAppsHere()

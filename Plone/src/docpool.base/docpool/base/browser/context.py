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
        """
        Determines all applications that are permitted for the object which is the current context of the
        dp_app_state view.
        The list of permitted apps is determined by the apps which may be configured in the doctype
        (if one is available) plus all implictly active apps.
        :param request:
        :return:
        """

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
        """
        Determines all apps that are actually effective for the object which is the current context of the
        dp_app_state view.
        The list is an intersection of the following sets of apps:
        - the apps permitted for the object type
        - the apps, which the user has actived via global preferencs (only if param filtered == true)
          which currently means: which are activated by navigating to an app-specific version of a docpool
        - the apps, which are supported on the object itself.
        :param request:
        :param filtered: If true, only return apps that are also in the user's preferences.
        :return:
        """
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
        """
        Returns the apps which are supported directly by the object which is the current context of the
        dp_app_state view.
        The list is determined by inspecting the local behaviours for the object and adding all implictly active apps.
        :return:
        """
        res = getattr(self.context, 'local_behaviors', [])[:]
        res.extend([app[0] for app in implicitApps()])
        return list(set(res))

    @memoize
    def appsPermittedForCurrentUser(self):
        """
        Determines all apps, that the current user has access to in the current context.
        The list is determined by evaluating the user roles and recognizing app specific roles of the format
        <AppName>User.
        For users with administrative rights all available apps are returned.
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
        Determines the list of apps, that are actually available to the current user in the current context.
        The list is an intersection of
        - the list of apps which the user has access permission for and
        - the list of apps which are actually supported in the current context (docpool).
        @return:
        """
        return list(
            set(self.appsPermittedForCurrentUser()).intersection(
                set(self.appsSupportedHere())
            )
        )

    def appsActivatedByCurrentUser(self):
        """
        Returns the app(s) which is/are activated by the user. Currently the active app is implicitly set
        by navigating to an app-specific version of a docpool.
        @return:
        """
        user = api.user.get_current()
        res = user.getProperty("apps") or [BASE_APP]
        # print "appsActivatedByCurrentUser: ", res
        return list(set(res))

    @memoize
    def effectiveAppsHere(self):
        """
        Returns the apps - actually currently only one max - that are in effect.
        This is determined as an intersection of the app(s) activated by the user (via navigation)
        and die apps that are supported in the current context (docpool).
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
        Returns the apps supported in the current context (docpool).
        Docpools can choose to support only a subset of available apps.
        @return:
        """
        try:
            return list(set(self.context.allSupportedApps()))
        except BaseException:
            return []

    @memoize
    def isCurrentlyActive(self, appname):
        """
        Checks for the app with the name appname, if that app is currently active.
        Can be used to determine the availability of app-specific features.
        @param appname: the name of the app to be checked
        @return:
        """
        return appname in self.effectiveAppsHere()

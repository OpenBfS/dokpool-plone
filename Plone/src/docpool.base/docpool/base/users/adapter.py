from plone.app.users.browser.personalpreferences import UserDataPanelAdapter


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
    """ """

    def get_dp(self):
        return self.context.getProperty("dp", "")

    def set_dp(self, value):
        return self.context.setMemberProperties({"dp": value})

    dp = property(get_dp, set_dp)

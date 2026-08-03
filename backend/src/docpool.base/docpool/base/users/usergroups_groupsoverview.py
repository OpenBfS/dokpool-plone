from Products.CMFPlone.controlpanel.browser.usergroups_groupsoverview import (
    GroupsOverviewControlPanel as GOCP,
)


class GroupsOverviewControlPanel(GOCP):
    def group_is_protected(self, groupinfo):
        protected = [
            "_Administrators",
            "_ContentAdministrators",
            "_DoksysUsers",
            "_ELANUsers",
            "_EventEditors",
            "_Members",
            "_Receivers",
            "_RodosContentAdministrators",
            "_RodosUsers",
            "_Senders",
            "_SituationReportAdmins",
        ]
        for suffix in protected:
            if groupinfo["groupid"].lower().endswith(suffix.lower()):
                return True
        return False

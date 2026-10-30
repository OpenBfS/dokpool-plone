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
            "_Journal1_Readers",
            "_Journal2_Readers",
            "_Journal3_Readers",
            "_Journal4_Readers",
            "_Journal5_Readers",
            "_Journal1_Editors",
            "_Journal2_Editors",
            "_Journal3_Editors",
            "_Journal4_Editors",
            "_Journal5_Editors",
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

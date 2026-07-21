from Products.CMFPlone.controlpanel.browser.usergroups_groupsoverview import (
    GroupsOverviewControlPanel as GOCP,
)


class GroupsOverviewControlPanel(GOCP):
    def group_is_protected(self, groupinfo):
        protected = [
            "_administrators",
            "_bfs_rei",
            "_bmu_rei",
            "_contentadministrators",
            "_doksysusers",
            "_elanusers",
            "_eventeditors",
            "_members",
            "_receivers",
            "_reicontentadministrators",
            "_reiusers",
            "_rodoscontentadministrators",
            "_rodosusers",
            "_senders",
            "_situationreportadmins",
            "administrators",
            "reviewers",
            "site administrators",
        ]
        for suffix in protected:
            if groupinfo["groupid"].lower().endswith(suffix):
                return True
        return False

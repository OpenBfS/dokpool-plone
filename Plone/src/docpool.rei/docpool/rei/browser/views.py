from collective.eeafaceted.dashboard.browser.overrides import DashboardFacetedTableView


class DokpoolDashboardFacetedTableView(DashboardFacetedTableView):
    """ Override to get weight sorting back
    """
    ignoreColumnWeight = False

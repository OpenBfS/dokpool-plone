from docpool.elan.config import ELAN_APP
from docpool.elan.utils import get_scenario_for_current_user
from plone import api
from plone.app.layout.viewlets.common import ViewletBase

import datetime
import dateutil


class TimezoneTableMixin:
    def get_local_time(self):
        return datetime.datetime.now()

    def get_utc_time(self):
        return datetime.datetime.now(datetime.UTC)

    def get_event_time(self):
        dp_app_state = api.content.get_view("dp_app_state", self.context, self.request)
        active_apps = dp_app_state.appsActivatedByCurrentUser()
        if ELAN_APP not in active_apps:
            return
        if event_uid := get_scenario_for_current_user(self.context):
            event = api.content.get(UID=event_uid)
            # TODO: Get timezone from event
            if timezone := getattr(event, "timezone", "Europe/Berlin"):
                if tz := dateutil.tz.gettz(timezone):
                    return datetime.datetime.now(tz)


class PortalFooter(TimezoneTableMixin, ViewletBase):
    pass

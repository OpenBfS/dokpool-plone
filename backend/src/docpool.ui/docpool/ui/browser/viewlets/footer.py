from plone.app.layout.viewlets.common import ViewletBase

import datetime


class PortalFooter(ViewletBase):
    def get_local_time(self):
        return datetime.datetime.now()

    def get_utc_time(self):
        return datetime.datetime.now(datetime.UTC)

    def get_jst_time(self):
        return datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=8)

from datetime import datetime
from docpool.base import DocpoolMessageFactory as _
from docpool.elan.utils import get_scenario_for_current_user
from docpool.ui.browser.listing import Listing
from plone import api
from plone.base.utils import safe_text
from Products.Five.browser import BrowserView


OVERVIEW_TILE_LIMIT = 2


class Overview(BrowserView):
    def __call__(self):
        return self.index()

    def selected_event(self):
        uid = get_scenario_for_current_user(self.context)
        if not uid:
            return None
        return api.content.get(UID=uid)

    def event_data(self):
        event = self.selected_event()
        if event is None:
            return {
                "has_event": False,
                "headline": "Kein Szenario ausgewählt",
                "placeholder": "Bitte wählen Sie ein Szenario aus, um die Ereignisdaten anzuzeigen.",
            }

        empty_value = "-"

        # Ereigniszeitpunkt und -dauer
        event_time_value = getattr(event, "TimeOfEvent", None)
        if event_time_value is not None and hasattr(event_time_value, "asdatetime"):
            event_time_value = event_time_value.asdatetime()
        if event_time_value is not None:
            plone_view = api.content.get_view("plone", self.context, self.request)
            date = plone_view.toLocalizedTime(event_time_value, long_format=False)
            time = plone_view.toLocalizedTime(event_time_value, time_only=True)
            event_time = f"{date} {time} ME(S)Z"

            now = datetime.now(event_time_value.tzinfo) if event_time_value.tzinfo else datetime.now()
            delta = now - event_time_value
            if delta.total_seconds() < 0:
                delta = -delta
            days = delta.days
            hours, remainder = divmod(delta.seconds, 3600)
            minutes = remainder // 60
            event_duration_label = f"{days}d {hours}h {minutes}min"
        else:
            event_time = empty_value
            event_duration_label = empty_value

        # Ereignisart
        if getattr(event, "EventType", None):
            event_type_value = event.event_type_title()
            event_type = safe_text(event_type_value).strip() if event_type_value is not None else empty_value
        else:
            event_type = empty_value

        # Betriebsart
        if getattr(event, "OperationMode", None):
            operation_mode_value = event.operation_mode_title()
            operation_mode = (
                safe_text(operation_mode_value).strip() if operation_mode_value is not None else empty_value
            )
        else:
            operation_mode = empty_value

        #  Status der Alarmierung
        alerting_status = getattr(event, "AlertingStatus", None)
        if alerting_status is not None:
            vocabulary = api.portal.get_vocabulary(
                "docpool.elan.vocabularies.AlertingStatus",
                context=event,
            )
            emergency_classification_value = vocabulary.getTerm(alerting_status).title
            emergency_classification = (
                safe_text(emergency_classification_value).strip()
                if emergency_classification_value is not None
                else empty_value
            )
        else:
            emergency_classification = empty_value

        # TODO How to get?
        reference_scenario = empty_value

        #  Szenario & Phase
        phase_value = getattr(event, "EventPhase", None)
        phase = safe_text(phase_value).strip() if phase_value is not None else empty_value
        phase = phase or empty_value

        description_value = getattr(event, "description", None)
        description = safe_text(description_value).strip() if description_value is not None else empty_value
        description = description or empty_value

        # Ereignisort
        location_relation = getattr(event, "EventLocation", None)
        location_obj = getattr(location_relation, "to_object", None)
        location = (
            safe_text(getattr(location_obj, "title", None) or "").strip() if location_obj is not None else ""
        )
        title_value = getattr(event, "title", None)
        title = safe_text(title_value).strip() if title_value is not None else empty_value
        title = location or title or empty_value

        # TODO
        coordinates_label = empty_value

        headline_values = [value for value in (title, coordinates_label) if value and value != empty_value]
        headline = " / ".join(headline_values) if headline_values else empty_value

        event_time_and_duration_values = [
            value for value in (event_time, event_duration_label) if value and value != empty_value
        ]
        event_time_and_duration = (
            " / ".join(event_time_and_duration_values) if event_time_and_duration_values else empty_value
        )

        return {
            "has_event": True,
            "headline": headline,
            "placeholder": "",
            "event_type": event_type,
            "event_time": event_time,
            "event_duration": event_duration_label,
            "event_time_and_duration": event_time_and_duration,
            "reference_scenario": reference_scenario,
            "emergency_classification": emergency_classification,
            "phase": phase,
            "description": description,
            "operation_mode": operation_mode,
        }


class OverviewTileListing(Listing):
    """Small listing variant used by the overview tiles."""

    filters = []
    tile_title = {"id": "", "title": ""}
    tile_query = {}

    def __call__(self):
        uids, modified = self.find(OVERVIEW_TILE_LIMIT)
        self.items = uids
        self.item_count = self.total_count
        self.modified = modified
        self.show_bulk_actions = False
        self.folder_uids = []
        self.other_uids = []
        return self.index()

    def update(self):
        self.query.update(self.tile_query)


class LatestSituationTile(OverviewTileListing):
    tile_title = {
        "id": "overview_tile_latest_situation",
        "title": _("overview_tile_latest_situation", default="Latest situation information"),
    }
    tile_query = {
        "dp_type": [
            "radiological_situation_report",
            "radiological_situation_report_draft",
            "situation_overview",
            "situation_overview_draft",
        ],
    }


class NotificationsTile(OverviewTileListing):
    tile_title = {
        "id": "overview_tile_notifications",
        "title": _("overview_tile_notifications", default="Notifications and plant information"),
    }
    tile_query = {
        "subcategory": ["official_notification"],
    }


# TODO Not needed in ELAN - Replace?
class RodosForecastsTile(OverviewTileListing):
    tile_title = {
        "id": "overview_tile_rodos_forecasts",
        "title": _("overview_tile_rodos_forecasts", default="RODOS forecasts"),
    }
    tile_query = {
        "UID": "_invalid_no_results_",
    }


class MeasurementsTile(OverviewTileListing):
    tile_title = {
        "id": "overview_tile_measurements",
        "title": _("overview_tile_measurements", default="Measurement results and strategies"),
    }
    tile_query = {
        "subcategory": ["Messstrategien"],
    }

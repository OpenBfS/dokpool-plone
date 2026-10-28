from datetime import datetime
from docpool.elan.utils import get_scenario_for_current_user
from docpool.ui import _
from docpool.ui.browser.listing import Listing
from plone import api
from plone.base.utils import safe_text
from Products.Five.browser import BrowserView
from pygeoif.exceptions import WKTParserError
from urllib.parse import urlencode

import json


OVERVIEW_TILE_LIMIT = 2


class ChronologyRedirect(BrowserView):
    def __call__(self):
        return self.request.response.redirect(f"{self.context.absolute_url()}/@@listing")


class Overview(BrowserView):
    def __call__(self):
        return self.index()

    def selected_event(self):
        uid = get_scenario_for_current_user(self.context)
        if not uid:
            return None
        return api.content.get(UID=uid)

    def map_data(self, event):
        try:
            point = event.coordinates()
        except (WKTParserError, TypeError, ValueError):
            return None
        if not point:
            return None

        longitude, latitude = point.x, point.y

        options = {
            "latitude": latitude,
            "longitude": longitude,
            "zoom": 10,
            "zoomcontrol": True,
            "fullscreencontrol": False,
            "useCluster": False,
            "map_layers": [],
            "default_map_layer": "OpenStreetMap.Mapnik",
            "addmarker": False,
            "geosearch": False,
            "locatecontrol": False,
            "autolocate": False,
            "minimap": False,
        }
        feature = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [longitude, latitude]},
            "properties": {
                "color": "red",
                "extraClasses": "overview-event-cross",
                "editable": False,
            },
        }
        return {
            "latitude": latitude,
            "longitude": longitude,
            "pattern_options": json.dumps(options),
            "geojson": json.dumps(feature),
        }

    def event_data(self):
        event = self.selected_event()
        if event is None:
            return {
                "has_event": False,
                "map": None,
                "headline": _("No scenario selected"),
                "placeholder": _("Please select a scenario to view the event data."),
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
            event_type_title = event.event_type_title()
            event_type_title = event_type_title if event_type_title is not None else empty_value
            event_type = event.EventType
        else:
            event_type_title = empty_value
            event_type = empty_value

        # Betriebsart
        if getattr(event, "OperationMode", None):
            operation_mode_value = event.operation_mode_title()
            operation_mode = operation_mode_value if operation_mode_value is not None else empty_value
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
                emergency_classification_value if emergency_classification_value is not None else empty_value
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

        map_data = self.map_data(event)
        location = safe_text(getattr(event, "EventLocation", None) or "").strip()
        title = safe_text(getattr(event, "title", None) or "").strip()
        headline = location or title or empty_value
        if map_data is not None:
            latitude, longitude = map_data["latitude"], map_data["longitude"]
            north_south = "N" if latitude >= 0 else "S"
            east_west = "E" if longitude >= 0 else "W"
            headline += f" / {north_south} {abs(latitude):.3f}, {east_west} {abs(longitude):.3f}"

        event_time_and_duration_values = [
            value for value in (event_time, event_duration_label) if value and value != empty_value
        ]
        event_time_and_duration = (
            " / ".join(event_time_and_duration_values) if event_time_and_duration_values else empty_value
        )

        return {
            "has_event": True,
            "map": map_data,
            "headline": headline,
            "placeholder": _("Please select a scenario to view the event data."),
            "event_type": event_type,
            "event_type_title": event_type_title,
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

    def listing_url(self):
        query = urlencode(
            {f"{name}:list": values for name, values in self.tile_query.items()},
            doseq=True,
            safe=":",
        )
        suffix = f"?{query}" if query else ""
        return f"{self.context.absolute_url()}/@@listing{suffix}"


# Aktuellste Lageinformationen
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


# Meldungen und Ereignisinformationen
class NotificationsTile(OverviewTileListing):
    tile_title = {
        "id": "overview_tile_notifications",
        "title": _("overview_tile_notifications", default="Reports and Event Information"),
    }
    tile_query = {
        "dp_type": ["official_notification", "additional_event_information"],
    }


# Maßnahmen und Informationen an Bevölkerung
class MeasuresInformationPublicTile(OverviewTileListing):
    tile_title = {
        "id": "overview_tile_public_information",
        "title": _("overview_tile_public_information", default="Measures and Information for the Public"),
    }
    tile_query = {"dp_type": ["response_action", "response_action_taken", "information_for_the_public"]}


# Messstrategien und Messempfehlungen
class MeasurementsTile(OverviewTileListing):
    tile_title = {
        "id": "overview_tile_measurements",
        "title": _("overview_tile_measurements", default="Measurement Strategies and Recommendations"),
    }
    tile_query = {
        "dp_type": ["measurement_recommendation", "measurement_strategy"],
    }

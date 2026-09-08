from plone.app.layout.viewlets.globalstatusmessage import GlobalStatusMessage as PloneGlobalStatusMessage
from zope.i18nmessageid import MessageFactory


_ = MessageFactory("plone")


MTYPES_DISPLAY = {
    "success": {
        "msg": _("statusmessage_mtype_success", default="Success:"),
        "icon": "check",
        "cssclass": "statusmessage statusmessage-success alert",
    },
    "info": {
        "msg": _("statusmessage_mtype_info", default="Info:"),
        "icon": "info-circle",
        "cssclass": "statusmessage statusmessage-info alert",
    },
    "warning": {
        "msg": _("statusmessage_mtype_warning", default="Warning:"),
        "icon": "exclamation-triangle",
        "cssclass": "statusmessage statusmessage-warning alert",
    },
    "error": {
        "msg": _("statusmessage_mtype_error", default="Error:"),
        "icon": "exclamation-triangle",
        "cssclass": "statusmessage statusmessage-error alert",
    },
    "danger": {
        "msg": _("statusmessage_mtype_danger", default="Danger:"),
        "icon": "exclamation-triangle",
        "cssclass": "statusmessage statusmessage-danger statusmessage-error alert",
    },
}


class GlobalStatusMessage(PloneGlobalStatusMessage):
    def display_info_for_mtype(self, mtype):
        return MTYPES_DISPLAY.get(mtype, MTYPES_DISPLAY["info"])

from logging import getLogger

import Acquisition
from Acquisition import aq_base
from docpool.base.utils import extendOptions
from plone.app.contenttypes.interfaces import IFile
from Products.CMFPlone.utils import base_hasattr, safe_hasattr
from Products.Five.browser import BrowserView
from Products.PageTemplates.PageTemplate import PageTemplate
from zope.component import getMultiAdapter
from zope.pagetemplate.interfaces import IPageTemplateSubclassing

logger = getLogger(__name__)


class OnTheFlyTemplate(Acquisition.Explicit, PageTemplate):
    def __call__(self, request, *args, **kwargs):
        if "args" not in kwargs:
            kwargs["args"] = args
        return self.pt_render(extra_context={"options": kwargs, "request": request})


class FlexibleView(BrowserView):
    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, context, request):
        """

        @param context:
        @param request:
        """
        super().__init__(context, request)

    #        self.extensions = self.context.myExtensions(request)

    def currentApplication(self):
        """ """
        app_defined_by_behaviour = getattr(self, "appname", None)
        if app_defined_by_behaviour:
            return app_defined_by_behaviour
        dp_app_state = getMultiAdapter((self, self.request), name="dp_app_state")
        active_apps = dp_app_state.appsActivatedByCurrentUser()
        if len(active_apps) > 0:
            return active_apps[0]
        return None

    def myViewSource(self, vtype):
        """
        Collects suitable macros/templates from apps, types, docs
        """
        doc = self.context
        dto = doc.docTypeObj()
        app = self.currentApplication()
        dtid = doc.getPortalTypeName().lower()
        if base_hasattr(doc, "typeName"):
            dtid = doc.typeName()
        if dto:
            dtid = dto.customViewTemplate
            if not dtid:
                dtid = dto.getId()
        else:
            dto = doc  # so that we can acquire stuff below
        data = ""

        if app:
            names = [
                f"{app}_{dtid}_{vtype}",
                f"{app}_{vtype}",
                f"{dtid}_{vtype}",
                "doc_%s" % vtype,
            ]
        else:
            names = [f"{dtid}_{vtype}", "doc_%s" % vtype]
        for n in names:
            if safe_hasattr(dto, n):
                o = aq_base(getattr(dto, n))
                logger.debug(
                    "Rendering template {} ({}) for {} ({})".format(
                        "/".join(o._filepath.split("/")[-2:]), vtype, doc, dtid
                    )
                )
                if IFile.providedBy(o):
                    f = o.file.open()
                    data = f.read()
                elif IPageTemplateSubclassing.providedBy(o):
                    data = o.read()
                return data
        return data

    def myView(self, vtype, **options):
        """
        Renders collected macros into a single template
        """
        # Get all macros / skin_templates for the context/app/...
        src = self.myViewSource(vtype)
        template = OnTheFlyTemplate()
        template = template.__of__(aq_base(self.context))
        template.pt_edit(src, "text/html")
        #        template.id = "flexible"
        # This "view" will run with security restrictions. The code will not be able
        # to access protected attributes and functions.
        # Todo WTF ? We do this to bypass security stuff?
        # BUT: code included via macros works!
        options = extendOptions(self.context, self.request, options)
        # Debug here
        return template(
            view=self, context=self.context, request=self.request, **options
        )

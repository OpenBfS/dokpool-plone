# -*- coding: utf-8 -*-
from Acquisition import aq_base
from docpool.base.utils import extendOptions
from plone.app.contenttypes.interfaces import IFile
from Products.CMFPlone.utils import base_hasattr
from Products.CMFPlone.utils import safe_hasattr
from Products.Five.browser import BrowserView
from Products.PageTemplates.PageTemplate import PageTemplate
from zope.component import getMultiAdapter
from zope.pagetemplate.interfaces import IPageTemplateSubclassing

import Acquisition


class OnTheFlyTemplate(Acquisition.Explicit, PageTemplate):
    def __call__(self, request, *args, **kwargs):
        if 'args' not in kwargs:
            kwargs['args'] = args
        return self.pt_render(
            extra_context={'options': kwargs, 'request': request})


class FlexibleView(BrowserView):
    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, context, request):
        """

        @param context:
        @param request:
        """
        super(FlexibleView, self).__init__(context, request)

    #        self.extensions = self.context.myExtensions(request)

    def currentApplication(self):
        """
        """
        app_defined_by_behaviour = getattr(self, "appname", None)
        if app_defined_by_behaviour:
            return app_defined_by_behaviour
        dp_app_state = getMultiAdapter(
            (self, self.request), name=u'dp_app_state')
        active_apps = dp_app_state.appsActivatedByCurrentUser()
        if len(active_apps) > 0:
            return active_apps[0]
        return None

    def myViewSource(self, vtype):
        """
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
                "%s_%s_%s" % (app, dtid, vtype),
                "%s_%s" % (app, vtype),
                "%s_%s" % (dtid, vtype),
                "doc_%s" % vtype,
            ]
        else:
            names = ["%s_%s" % (dtid, vtype), "doc_%s" % vtype]
        # for n in names:
        # print n
        for n in names:
            if safe_hasattr(dto, n):
                o = aq_base(getattr(dto, n))
                if IFile.providedBy(o):
                    f = o.file.open()
                    data = f.read()
                elif IPageTemplateSubclassing.providedBy(o):
                    data = o.read()
                return data
        return data

    def myView(self, vtype, **options):
        """
        """
        src = self.myViewSource(vtype)
        template = OnTheFlyTemplate()
        template = template.__of__(aq_base(self.context))
        template.pt_edit(src, "text/html")
        #        template.id = "flexible"
        # This "view" will run with security restrictions. The code will not be able
        # to access protected attributes and functions.
        # BUT: code included via macros works!
        options = extendOptions(self.context, self.request, options)
        # Debug here
        return template(
            view=self, context=self.context, request=self.request, **options
        )

from logging import getLogger

from Acquisition import aq_base
from docpool.base.utils import extendOptions
from plone.app.contenttypes.interfaces import IFile
from Products.CMFPlone.utils import base_hasattr, safe_hasattr
from Products.Five.browser import BrowserView
from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.pagetemplate.interfaces import IPageTemplateSubclassing

logger = getLogger(__name__)


class OnTheFlyTemplate(ZopePageTemplate):
    def __call__(self, request, *args, **kwargs):
        if "args" not in kwargs:
            kwargs["args"] = args
        return self.pt_render(extra_context={"options": kwargs, "request": request})


class FlexibleView(BrowserView):
    __allow_access_to_unprotected_subobjects__ = 1

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

    def find_view(self, vtype):
        """Find correct view for that doc of that type with that view-type

        For that we need:
        * obj: the context obj, either a DPDocument or something else like a SituationReport
        * doctype: the doctype/template for that DPDocument (usually in in /config/dtypes/xxx) or nothing
        * vtype: the view-type, usually "meta" or "listitem"
        * app: the currently active app (elan/rei/doksys) or nothing
        """
        document = self.context
        app = self.currentApplication()
        doctype = document.docTypeObj()

        if doctype:
            typename = doctype.customViewTemplate or doctype.id
        elif base_hasattr(document, "typeName"):
            # Some (non-DPDocument) may have custom typeNames, e.g. "SituationReport" is called "sitrep"
            typename = document.typeName()
        else:
            typename = document.portal_type.lower()

        # Check view by order of specification
        if app:
            names = [
                f"{app}_{typename}_{vtype}",
                f"{app}_{vtype}",
                f"{typename}_{vtype}",
                f"doc_{vtype}",
            ]
        else:
            names = [
                f"{typename}_{vtype}",
                f"doc_{vtype}",
            ]

        for name in names:
            # Look for a BrowserView first (see #4840)
            view = queryMultiAdapter((document, self.request), name=name)
            if view is not None:
                logger.info(
                    "Rendering view %s (%s) for %r (%s)",
                    name,
                    view.index.filename,
                    document,
                    typename,
                )
                return view

    def render_view_or_template(self, vtype, **options):
        """
        Collects suitable macros/templates from apps, types, docs
        """
        document = self.context
        app = self.currentApplication()
        doctype = document.docTypeObj()

        if doctype:
            typename = doctype.customViewTemplate or doctype.id
        elif base_hasattr(document, "typeName"):
            # Some (non-DPDocument) may have custom typeNames, e.g. "SituationReport" is called "sitrep"
            typename = document.typeName()
        else:
            typename = document.portal_type.lower()

        # Check view by order of specification
        if app:
            names = [
                f"{app}_{typename}_{vtype}",
                f"{app}_{vtype}",
                f"{typename}_{vtype}",
                f"doc_{vtype}",
            ]
        else:
            names = [
                f"{typename}_{vtype}",
                f"doc_{vtype}",
            ]

        for name in names:
            # 1. Check for a BrowserView (usually only a registered template)
            view = queryMultiAdapter((document, self.request), name=name)
            if view is not None:
                logger.info(
                    "Rendering view %s (%s) for %r (%s)",
                    name,
                    view.index.filename,
                    document,
                    typename,
                )
                if view is not None:
                    # add additional info uses in the templates
                    options = extendOptions(self.context, self.request, options)
                    # self is the adapter for the obj wrapped in it's behavior
                    # e.g. IREIDoc(self.context) => <docpool.rei.behaviors.reidoc.REIDoc object at 0x1213c1520>
                    # because these are registered as the behavior-factory and inherit from FlexibleView
                    # This (options/view) is used in the templates to call methods on these adapters
                    # TODO: Maye we need to refactor all behaviors to make the templates more sane.
                    options["view"] = self
                    return view(**options)

            # 2. Acquire a skin template (deprecated)
            data = ""
            if not doctype:
                # to acqucire the template from
                doctype = document
            if safe_hasattr(doctype, name):
                template = aq_base(getattr(doctype, name))
                logger.info(
                    "Rendering template %s (%s) for %r (%s)",
                    "/".join(template._filepath.split("/")[-2:]),
                    vtype,
                    document,
                    typename,
                )
                if IFile.providedBy(template):
                    f = template.file.open()
                    data = f.read()
                elif IPageTemplateSubclassing.providedBy(template):
                    data = template.read()
                template = OnTheFlyTemplate(id="flexible", text=data)
                template = template.__of__(self.context)
                # This "view" will run with security restrictions. The code will not be able
                # to access protected attributes and functions.
                # Todo WTF ? We do this to bypass security stuff?
                # BUT: code included via macros works!
                options = extendOptions(self.context, self.request, options)
                # Debug here
                return template(
                    view=self, context=self.context, request=self.request, **options
                )

    def myView(self, vtype, **options):
        """
        Renders collected macros into a single template
        """
        return self.render_view_or_template(vtype, **options)

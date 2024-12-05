from docpool.base.utils import extendOptions
from logging import getLogger
from plone.base.utils import base_hasattr
from Products.Five.browser import BrowserView
from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter


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
            # Some (non-DPDocument) may have custom typeNames, e.g. "SituationReport" is
            # called "sitrep"
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
            # Check for a BrowserView (usually only a registered template)
            view = queryMultiAdapter((document, self.request), name=name)
            if view is not None:
                logger.debug(
                    "Rendering view %s (%s) for %r (%s)",
                    name,
                    view.index.filename,
                    document,
                    typename,
                )
                # add additional info uses in the templates
                options = extendOptions(self.context, self.request, options)
                # self is the adapter for the obj wrapped in it's behavior
                # e.g. IREIDoc(self.context) => <docpool.rei.behaviors.reidoc.REIDoc
                # object at 0x1213c1520> because these are registered as the
                # behavior-factory and inherit from FlexibleView
                # This (options/view) is used in the templates to call methods on these
                # adapters
                # TODO: Maye we need to refactor all behaviors to make the templates
                # more sane.
                options["view"] = self
                return view(**options)

    def myView(self, vtype, **options):
        """
        Renders collected macros into a single template
        """
        return self.render_view_or_template(vtype, **options)

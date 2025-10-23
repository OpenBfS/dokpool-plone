from Acquisition import aq_base
from Acquisition import aq_inner
from logging import getLogger
from plone import api
from plone.base import PloneMessageFactory as _
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


logger = getLogger(__name__)


class ReviewHistoryView(BrowserView):
    """Workflow History (no versions). Taken mostly from
    plone.app.layout.viewlets.content.WorkflowHistoryViewlet.

    Differences:
    * Translate transitions from placeful workflows as well
    * Custom template
    * WorkflowHistoryViewlet is not registered as a view
    """

    index = ViewPageTemplateFile("templates/review_history.pt")

    def __call__(self):
        self.history = self.workflowHistory(complete=False)
        return self.index()

    def workflowHistory(self, complete=True):
        """Return workflow history of this context."""
        context = aq_inner(self.context)
        # check if the current user has the proper permissions
        if not (
            _checkPermission("Request review", context) or _checkPermission("Review portal content", context)
        ):
            return []

        portal_workflow = api.portal.get_tool("portal_workflow")
        portal_membership = api.portal.get_tool("portal_membership")

        # get currently active workflow
        chain = portal_workflow.getChainFor(context)
        wf_id = chain[0] if chain else None
        self.wf = portal_workflow.getWorkflowById(wf_id)

        review_history = []

        try:
            # get total history
            review_history = portal_workflow.getInfoFor(context, "review_history")

            if not complete:
                # filter out automatic transitions.
                review_history = [r for r in review_history if r["action"]]
            else:
                review_history = list(review_history)

            anon = _("label_anonymous_user", default="Anonymous User")

            for r in review_history:
                r["type"] = "workflow"
                r["transition_title"] = self.getTitleForTransition(r["action"]) or _("Create")
                r["state_title"] = self.getTitleForState(r["review_state"])
                actorid = r["actor"]
                r["actorid"] = actorid
                if actorid is None:
                    # action performed by an anonymous user
                    r["actor"] = {"username": anon, "fullname": anon}
                    r["actor_home"] = ""
                else:
                    r["actor"] = portal_membership.getMemberInfo(actorid)
            review_history.reverse()

        except WorkflowException:
            logger.debug(
                "docpool.base.browser.review_history: %s has no associated workflow",
                context.absolute_url(),
            )

        return review_history

    def getTitleForState(self, state_name):
        states = self.wf.states
        state = getattr(states, state_name, None)
        if state is not None:
            return getattr(aq_base(state), "title", None) or state_name
        return state_name

    def getTitleForTransition(self, trans_name):
        transitions = self.wf.transitions
        trans = getattr(transitions, trans_name, None)
        if trans is not None:
            return getattr(aq_base(trans), "actbox_name", None) or trans_name
        return trans_name


class FullReviewHistoryView(BrowserView):
    """Workflow History (no versions). Taken mostly from
    plone.app.layout.viewlets.content.WorkflowHistoryViewlet.

    Differences:
    * Show history for all workflows (even if the workflow changed over time)
    * Translate transitions from placeful workflows as well
    * Custom template
    * WorkflowHistoryViewlet is not registered as a view
    """

    index = ViewPageTemplateFile("templates/full_review_history.pt")

    def __call__(self):
        self.history = self.workflowHistory(complete=True)
        return self.index()

    def workflowHistory(self, complete=True):
        """Return workflow history of this context."""
        context = aq_inner(self.context)
        # check if the current user has the proper permissions
        if not (
            _checkPermission("Request review", context) or _checkPermission("Review portal content", context)
        ):
            return

        portal_workflow = api.portal.get_tool("portal_workflow")
        portal_membership = api.portal.get_tool("portal_membership")

        full_review_history = {}

        # get currently active workflow
        workflow_history = getattr(aq_base(context), "workflow_history", {})
        for wf_id in workflow_history.keys():
            workflow = portal_workflow.getWorkflowById(wf_id)
            review_history = []

            try:
                # get total history
                review_history = portal_workflow.getInfoFor(context, "review_history", wf_id=wf_id)

                if not complete:
                    # filter out automatic transitions.
                    review_history = [r for r in review_history if r["action"]]
                else:
                    review_history = list(review_history)

                anon = _("label_anonymous_user", default="Anonymous User")

                for r in review_history:
                    r["type"] = "workflow"
                    if r["action"]:
                        r["transition_title"] = getTitleForTransition(workflow, r["action"])
                    else:
                        r["transition_title"] = _("Create")
                    r["state_title"] = getTitleForState(workflow, r["review_state"])
                    actorid = r["actor"]
                    r["actorid"] = actorid
                    if actorid is None:
                        # action performed by an anonymous user
                        r["actor"] = {"username": anon, "fullname": anon}
                        r["actor_home"] = ""
                    else:
                        r["actor"] = portal_membership.getMemberInfo(actorid)
                review_history.reverse()

            except WorkflowException:
                logger.debug(
                    "docpool.base.browser.review_history: %s has no associated workflow",
                    context.absolute_url(),
                )

            full_review_history[wf_id] = review_history
        return dict(reversed(list(full_review_history.items())))

    def workflow_title(self, wf_id):
        portal_workflow = api.portal.get_tool("portal_workflow")
        workflow = portal_workflow.getWorkflowById(wf_id)
        if workflow is not None:
            return getattr(aq_base(workflow), "title", None) or wf_id
        return wf_id


def getTitleForState(workflow, state_name):
    states = workflow.states
    state = getattr(states, state_name, None)
    if state is not None:
        return getattr(aq_base(state), "title", None) or state_name
    return state_name


def getTitleForTransition(workflow, trans_name):
    transitions = workflow.transitions
    trans = getattr(transitions, trans_name, None)
    if trans is not None:
        return getattr(aq_base(trans), "actbox_name", None) or trans_name
    return trans_name

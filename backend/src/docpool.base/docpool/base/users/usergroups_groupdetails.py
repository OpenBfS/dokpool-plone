from Acquisition import aq_inner
from Acquisition import ImplicitAcquisitionWrapper
from docpool.base import DocpoolMessageFactory as _
from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.base.marker import IJournalContainerMarker
from docpool.base.vocabularies import DocTypeVocabularyFactory
from logging import getLogger
from plone import api
from plone.app.z3cform.widgets.orderedselect import OrderedSelectFieldWidget
from plone.base import PloneMessageFactory as PMF
from plone.protect import CheckAuthenticator
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.controlpanel.browser.usergroups_groupdetails import GroupDetailsControlPanel as GDCP
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form.interfaces import IContextAware
from zope import schema
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider
from zope.schema.interfaces import IContextSourceBinder

logger = getLogger(__name__)


@provider(IContextSourceBinder)
def possible_doctypes(context):
    return DocTypeVocabularyFactory(context, ids=True)


class IGroupDetails(Interface):
    allowedDocTypes = schema.List(
        title=_("heading_allowed_doctypes", default="Allowed document types"),
        description=_(
            "description_allowed_doctypes",
            default="Allowed document types for this group.",
        ),
        required=True,
        missing_value=[],
        value_type=schema.Choice(source=possible_doctypes),
    )


@implementer(IGroupDetails)
class GroupProxy:
    allowedDocTypes = None


class GroupDetailsControlPanel(GDCP):
    def __call__(self):
        context = aq_inner(self.context)

        self.gtool = getToolByName(context, "portal_groups")
        self.gdtool = getToolByName(context, "portal_groupdata")
        self.regtool = getToolByName(context, "portal_registration")
        self.groupname = getattr(self.request, "groupname", None)
        self.grouproles = self.request.set("grouproles", [])
        self.group = self.gtool.getGroupById(self.groupname)
        self.grouptitle = self.groupname
        if self.group is not None:
            self.grouptitle = self.group.getGroupTitleOrName()

        self.request.set("grouproles", self.group.getRoles() if self.group else [])

        self.setup_allowed_doctypes_widget()

        submitted = self.request.form.get("form.submitted") and self.request.form.get("form.button.Save")
        if submitted:
            CheckAuthenticator(self.request)

            msg = PMF("No changes made.")
            self.group = None

            title = self.request.form.get("title", None)
            description = self.request.form.get("description", None)
            addname = self.request.form.get("addname", None)

            if addname:
                if not self.regtool.isMemberIdAllowed(addname):
                    msg = PMF("The group name you entered is not valid.")
                    IStatusMessage(self.request).add(msg, "error")
                    return self.index()

                #######
                # BfS: modifications for local user management:
                # Automatically change id and titel with prefix
                # when we are inside a DocumentPool
                props = {"title": title, "description": description}
                if (dp := self.context).portal_type == "DocumentPool":
                    prefix = dp.prefix or dp.getId()
                    dp_title = dp.Title()
                    addname = f"{prefix}_{addname}"
                    title = f"{title} ({dp_title})"
                    # Add reference to DocumentPool here
                    props["dp"] = dp.UID()
                    # Put it in the request for later processing (see below)
                    self.request.set("dp", dp.UID())
                #######

                success = self.gtool.addGroup(
                    addname,
                    (),
                    (),
                    properties=props,
                    title=title,
                    description=description,
                    REQUEST=self.request,
                )
                if not success:
                    msg = PMF(
                        "Could not add group ${name}, perhaps a user or group with this name already exists.",
                        mapping={"name": addname},
                    )
                    IStatusMessage(self.request).add(msg, "error")
                    return self.index()

                self.group = self.gtool.getGroupById(addname)
                msg = PMF("Group ${name} has been added.", mapping={"name": addname})

            elif self.groupname:
                self.gtool.editGroup(
                    self.groupname,
                    roles=None,
                    groups=None,
                    title=title,
                    description=description,
                    REQUEST=context.REQUEST,
                )
                self.group = self.gtool.getGroupById(self.groupname)
                msg = PMF("Changes saved.")

            else:
                msg = PMF("Group name required.")

            processed = {}
            for id, property in self.gdtool.propertyItems():  # noqa: B007
                # BfS: Here we take the "dp" from the request (set above)
                processed[id] = self.request.get(id, None)
                try:
                    processed["dp"] = context.UID()
                except BaseException:
                    pass

            if self.group:
                # for what reason ever, the very first group created does not
                # exist
                self.group.setGroupProperties(processed)

            if "journalentry" in processed.get("allowedDocTypes", []):
                # make sure that group has a folder for journal entries
                create_journalfolder(context, self.group)

            IStatusMessage(self.request).add(msg, type=(self.group and "info") or "error")
            if self.group and not self.groupname:
                target_url = "{}/{}".format(
                    self.context.absolute_url(),
                    "@@usergroup-groupprefs",
                )
                self.request.response.redirect(target_url)
                return ""

        return self.index()

    def setup_allowed_doctypes_widget(self):
        group_proxy = ImplicitAcquisitionWrapper(GroupProxy(), self.context)
        group_proxy.allowedDocTypes = self.group.getProperty("allowedDocTypes")
        field = IGroupDetails["allowedDocTypes"].bind(group_proxy)
        self.doctypes_widget = OrderedSelectFieldWidget(field, self.request)
        alsoProvides(self.doctypes_widget, IContextAware)
        self.doctypes_widget.context = group_proxy
        self.doctypes_widget.update()


def create_journalfolder(context, group):
    if context.portal_type != "DocumentPool":
        return
    try:
        group_folder = context["content"]["Groups"][group.id]
    except KeyError:
        logger.error("Could not find group folder for %s", group.id)
        return

    if journal_folder := group_folder.get("journal", None):
        # Check if existing journal folder has correct settings.
        if journal_folder.portal_type != "SimpleFolder":
            logger.error("Journal folder is not a SimpleFolder but %s", journal_folder.portal_type)
            return
        if not IJournalContainerMarker.providedBy(journal_folder):
            logger.error("IJournalContainerMarker not provided by Journal folder")
            return
        if journal_folder.local_behaviors != ["elan"]:
            logger.error("Journal folder is not elan")
            return
        if journal_folder.allowedDocTypes != ["journalentry"]:
            logger.error("Journal does not allow journalentry but %s", journal_folder.allowedDocTypes)
            return

    else:
        title = "Tagebuch " + group.getProperty("title")
        journal_folder = api.content.create(
            container=group_folder,
            type="SimpleFolder",
            title=title,
            id="journal",
        )
        # apply marker interface
        alsoProvides(journal_folder, IJournalContainerMarker)
        ILocalBehaviorSupport(journal_folder).local_behaviors = ["elan"]
        journal_folder.allowedDocTypes = ["journalentry"]

        # Make sure that journalentry is only allowed here
        if group_folder.allowedDocTypes and "journalentry" in group_folder.allowedDocTypes:
            # remove journalentry from gf
            group_folder.allowedDocTypes.remove("journalentry")
        elif not group_folder.allowedDocTypes:
            # allow all types except journalentry
            all_allowed = [i for i in group.getProperty("allowedDocTypes", [])]
            all_allowed.remove("journalentry")
            group_folder.allowedDocTypes = all_allowed

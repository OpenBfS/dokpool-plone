from Acquisition import aq_inner
from plone.protect import CheckAuthenticator
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.controlpanel.browser.usergroups_groupdetails import (
    GroupDetailsControlPanel as GDCP,
)
from Products.CMFPlone.utils import base_hasattr
from Products.statusmessages.interfaces import IStatusMessage


class GroupDetailsControlPanel(GDCP):
    def __call__(self):
        context = aq_inner(self.context)

        self.gtool = getToolByName(context, 'portal_groups')
        self.gdtool = getToolByName(context, 'portal_groupdata')
        self.regtool = getToolByName(context, 'portal_registration')
        self.groupname = getattr(self.request, 'groupname', None)
        self.grouproles = self.request.set('grouproles', [])
        self.group = self.gtool.getGroupById(self.groupname)
        self.grouptitle = self.groupname
        if self.group is not None:
            self.grouptitle = self.group.getGroupTitleOrName()

        self.request.set(
            'grouproles',
            self.group.getRoles() if self.group else [])

        submitted = self.request.form.get('form.submitted', False)
        if submitted:
            CheckAuthenticator(self.request)

            msg = _(u'No changes made.')
            self.group = None

            title = self.request.form.get('title', None)
            description = self.request.form.get('description', None)
            addname = self.request.form.get('addname', None)

            if addname:
                if not self.regtool.isMemberIdAllowed(addname):
                    msg = _(u'The group name you entered is not valid.')
                    IStatusMessage(self.request).add(msg, 'error')
                    return self.index()

                #######
                # BfS: modifications for local user management:
                # Automatically change id and titel with prefix
                # when we are inside a DocumentPool
                if base_hasattr(self.context, "myDocumentPool"):
                    dp = self.context
                    prefix = dp.prefix or dp.getId()
                    prefix = str(prefix)
                    dp_title = dp.Title()

                    addname = "%s_%s" % (prefix, addname)
                    title = "%s (%s)" % (title, dp_title)
                    isDP = True
                else:
                    isDP = False

                if isDP:
                    # Add reference to DocumentPool here
                    props = {
                        'title': title,
                        'description': description,
                        'dp': dp.UID()}
                    # Put it in the request for later processing (see below)
                    self.request.set("dp", dp.UID())
                else:
                    props = {'title': title, 'description': description}

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
                    msg = _(
                        u'Could not add group ${name}, perhaps a user or group with '
                        u'this name already exists.',
                        mapping={u'name': addname},
                    )
                    IStatusMessage(self.request).add(msg, 'error')
                    return self.index()

                self.group = self.gtool.getGroupById(addname)
                msg = _(
                    u'Group ${name} has been added.',
                    mapping={
                        u'name': addname})

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
                msg = _(u'Changes saved.')

            else:
                msg = _(u'Group name required.')

            processed = {}
            for id, property in self.gdtool.propertyItems():
                # BfS: Here we take the "dp" from the request (set above)
                processed[id] = self.request.get(id, None)
                try:
                    processed['dp'] = context.UID()
                except BaseException:
                    pass

            if self.group:
                # for what reason ever, the very first group created does not
                # exist
                self.group.setGroupProperties(processed)

            IStatusMessage(
                self.request).add(
                msg, type=self.group and 'info' or 'error')
            if self.group and not self.groupname:
                target_url = '%s/%s' % (
                    self.context.absolute_url(),
                    '@@usergroup-groupprefs',
                )
                self.request.response.redirect(target_url)
                return ''

        return self.index()

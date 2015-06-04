from zope.interface import Interface
from zope.component import getUtility, getAdapter
from zope.schema import getFieldNamesInOrder

from five.formlib.formbase import PageForm
from zope import schema
from zope.formlib import form
from zope.formlib.boolwidgets import CheckBoxWidget
from zope.formlib.interfaces import InputErrors
from zope.formlib.interfaces import WidgetInputError
from zope.formlib.textwidgets import ASCIIWidget
from zope.component import getMultiAdapter

from AccessControl import getSecurityManager
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString, safe_unicode
from Products.CMFPlone import PloneMessageFactory as _

from ZODB.POSException import ConflictError
from zExceptions import Forbidden

from Products.statusmessages.interfaces import IStatusMessage

from plone.app.users.userdataschema import IUserDataSchemaProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.controlpanel.widgets import MultiCheckBoxVocabularyWidget
from plone.app.users.browser.register import BaseRegistrationForm,\
    CantSendMailWidget

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.site.hooks import getSite
from plone.protect import CheckAuthenticator

import logging

# Define constants from the Join schema that should be added to the
# vocab of the join fields setting in usergroupssettings controlpanel.
JOIN_CONST = ['username', 'password', 'email', 'mail_me']


class IRegisterSchema(Interface):

    username = schema.ASCIILine(
        title=_(u'label_user_name', default=u'User Name'),
        description=_(u'help_user_name_creation_casesensitive',
                      default=u"Enter a user name, usually something "
                               "like 'jsmith'. "
                               "No spaces or special characters. "
                               "Usernames and passwords are case sensitive, "
                               "make sure the caps lock key is not enabled. "
                               "This is the name used to log in."))

    password = schema.Password(
        title=_(u'label_password', default=u'Password'),
        description=_(u'help_password_creation',
                      default=u'Enter your new password.'))

    password_ctl = schema.Password(
        title=_(u'label_confirm_password',
                default=u'Confirm password'),
        description=_(u'help_confirm_password',
                      default=u"Re-enter the password. "
                      "Make sure the passwords are identical."))

    mail_me = schema.Bool(
        title=_(u'label_mail_password',
                default=u"Send a confirmation mail with a link to set the "
                u"password"),
        required=False,
        default=False)


class IAddUserSchema(Interface):

    groups = schema.List(
        title=_(u'label_add_to_groups',
                default=u'Add to the following groups:'),
        description=u'',
        required=False,
        value_type=schema.Choice(vocabulary='ESD Group Ids'))






def getGroupIds(context):
    site = getSite()
    groups_tool = getToolByName(site, 'portal_groups')
    groups = groups_tool.listGroups()
    # Get group id, title tuples for each, omitting virtual group
    # 'AuthenticatedUsers'
    terms = []
    for g in groups:
        # Filter local groups
        if not g.getProperty("dp") == context.UID():
            continue
        if g.id.find("Members") > -1:
            continue
        if g.id == 'AuthenticatedUsers':
            continue
        is_zope_manager = getSecurityManager().checkPermission(
            ManagePortal, context)
        if 'Manager' in g.getRoles() and not is_zope_manager:
            continue

        group_title = safe_unicode(g.getGroupTitleOrName())
        if group_title != g.id:
            title = u'%s (%s)' % (group_title, g.id)
        else:
            title = group_title
        terms.append(SimpleTerm(g.id, g.id, title))
    # Sort by title
    terms.sort(key=lambda x: normalizeString(x.title))
    return SimpleVocabulary(terms)

@property
def form_fields(self):
    """ form_fields is dynamic in this form, to be able to handle
    different join styles.
    """
    portal_props = getToolByName(self.context, 'portal_properties')
    props = portal_props.site_properties
    use_email_as_login = props.getProperty('use_email_as_login')
    registration_fields = list(props.getProperty(
            'user_registration_fields', []))

    # Check on required join fields
    if not 'username' in registration_fields and not use_email_as_login:
        registration_fields.insert(0, 'username')

    if 'username' in registration_fields and use_email_as_login:
        registration_fields.remove('username')

#        if not 'email' in registration_fields:
#            # Perhaps only when use_email_as_login is true, but also
#            # for some other cases; the email field has always been
#            # required.
#            registration_fields.append('email')

    if not 'password' in registration_fields:
        if 'username' in registration_fields:
            base = registration_fields.index('username')
        else:
            base = registration_fields.index('email')
        registration_fields.insert(base + 1, 'password')

    # Add password_ctl after password
    if not 'password_ctl' in registration_fields:
        registration_fields.insert(
            registration_fields.index('password') + 1, 'password_ctl')

#        # Add email_me after password_ctl
#        if not 'mail_me' in registration_fields:
#            registration_fields.insert(
#                registration_fields.index('password_ctl') + 1, 'mail_me')

    # We need fields from both schemata here.
    util = getUtility(IUserDataSchemaProvider)
    schema = util.getSchema()

    all_fields = form.Fields(schema) + form.Fields(IRegisterSchema)

#        if use_email_as_login:
#            all_fields['email'].custom_widget = EmailAsLoginWidget
#        else:
#            all_fields['email'].custom_widget = EmailWidget

    # Make sure some fields are really required; a previous call
    # might have changed the default.
    for name in ('password', 'password_ctl'):
        all_fields[name].field.required = True

    # Change the password description based on PAS Plugin
    # The user needs a list of instructions on what kind of password is required.
    # We'll reuse password errors as instructions e.g. "Must contain a letter and a number".
    # Assume PASPlugin errors are already translated
    if all_fields.get('password',None):
        registration = getToolByName(self.context, 'portal_registration')
        err_str = registration.testPasswordValidity('')
        if err_str:
            msgid = _(u'Enter your new password. ${errors}', mapping=dict(errors=err_str))
            all_fields['password'].field.description = self.context.translate(msgid)

    # Pass the list of join form fields as a reference to the
    # Fields constructor, and return.
    return form.Fields(*[all_fields[id] for id in registration_fields])

BaseRegistrationForm.form_fields = form_fields

def handle_join_success(self, data):
    # portal should be acquisition wrapped, this is needed for the schema
    # adapter below
    portal = getToolByName(self.context, 'portal_url').getPortalObject()
    registration = getToolByName(self.context, 'portal_registration')
    portal_props = getToolByName(self.context, 'portal_properties')
    mt = getToolByName(self.context, 'portal_membership')
    props = portal_props.site_properties
    use_email_as_login = props.getProperty('use_email_as_login')

    if use_email_as_login:
        # The username field is not shown as the email is going to
        # be the username, but the field *is* needed further down
        # the line.
        data['username'] = data['email']
        # Set username in the form; at least needed for logging in
        # immediately when password reset is bypassed.
        self.request.form['form.username'] = data['email']

    user_id = data['username']
    password = data.get('password') or registration.generatePassword()

    try:
        registration.addMember(user_id, password, REQUEST=self.request)
    except (AttributeError, ValueError), err:
        logging.exception(err)
        IStatusMessage(self.request).addStatusMessage(err, type="error")
        return

    # set additional properties using the user schema adapter
    schema = getUtility(IUserDataSchemaProvider).getSchema()

    adapter = getAdapter(portal, schema)
    adapter.context = mt.getMemberById(user_id)

    for name in getFieldNamesInOrder(schema):
        if name in data:
            setattr(adapter, name, data[name])

    if data.get('mail_me') or (portal.validate_email and
                               not data.get('password')):
        # We want to validate the email address (users cannot
        # select their own passwords on the register form) or the
        # admin has explicitly requested to send an email on the
        # 'add new user' form.
        try:
            # When all goes well, this call actually returns the
            # rendered mail_password_response template.  As a side
            # effect, this removes any status messages added to
            # the request so far, as they are already shown in
            # this template.
            response = registration.registeredNotify(user_id)
            return response
        except ConflictError:
            # Let Zope handle this exception.
            raise
        except Exception:
            ctrlOverview = getMultiAdapter((portal, self.request),
                                           name='overview-controlpanel')
            mail_settings_correct = not ctrlOverview.mailhost_warning()
            if mail_settings_correct:
                # The email settings are correct, so the most
                # likely cause of an error is a wrong email
                # address.  We remove the account:
                # Remove the account:
                self.context.acl_users.userFolderDelUsers(
                    [user_id], REQUEST=self.request)
                IStatusMessage(self.request).addStatusMessage(
                    _(u'status_fatal_password_mail',
                      default=u"Failed to create your account: we were "
                      "unable to send instructions for setting a password "
                      "to your email address: ${address}",
                      mapping={u'address': data.get('email', '')}),
                    type='error')
                return
            else:
                # This should only happen when an admin registers
                # a user.  The admin should have seen a warning
                # already, but we warn again for clarity.
                IStatusMessage(self.request).addStatusMessage(
                    _(u'status_nonfatal_password_mail',
                      default=u"This account has been created, but we "
                      "were unable to send instructions for setting a "
                      "password to this email address: ${address}",
                      mapping={u'address': data.get('email', '')}),
                    type='warning')
                return

    return


class AddUserForm(BaseRegistrationForm):

    label = _(u'heading_add_user_form', default=u'Add New User')
    description = u""
    template = ViewPageTemplateFile('newuser_form.pt')


    @property
    def form_fields(self):
        defaultFields = super(AddUserForm, self).form_fields

#        # The mail_me field needs special handling depending on the
#        # validate_email property and on the correctness of the mail
#        # settings.
#        portal = getUtility(ISiteRoot)
#        ctrlOverview = getMultiAdapter((portal, self.request),
#                                       name='overview-controlpanel')
#        mail_settings_correct = not ctrlOverview.mailhost_warning()
#        if not mail_settings_correct:
#            defaultFields['mail_me'].custom_widget = CantSendMailWidget
#        else:
#            # Make the password fields optional: either specify a
#            # password or mail the user (or both).  The validation
#            # will check that at least one of the options is chosen.
#            defaultFields['password'].field.required = False
#            defaultFields['password_ctl'].field.required = False
#            if portal.getProperty('validate_email', True):
#                defaultFields['mail_me'].field.default = True
#            else:
#                defaultFields['mail_me'].field.default = False
#
        # Append the manager-focused fields
        allFields = defaultFields + form.Fields(IAddUserSchema)

        allFields['groups'].custom_widget = MultiCheckBoxVocabularyWidget

        return allFields
    

    # Actions validators
    def validate_registration(self, action, data):
        """
        specific business logic for this join form
        note: all this logic was taken directly from the old
        validate_registration.py script in
        Products/CMFPlone/skins/plone_login/join_form_validate.vpy
        """

        # CSRF protection
        CheckAuthenticator(self.request)

        registration = getToolByName(self.context, 'portal_registration')

        errors = super(BaseRegistrationForm, self).validate(action, data)
        # ConversionErrors have no field_name attribute... :-(
        error_keys = [error.field_name for error in errors
                      if hasattr(error, 'field_name')]

        form_field_names = [f.field.getName() for f in self.form_fields]

        portal = getUtility(ISiteRoot)
        portal_props = getToolByName(self.context, 'portal_properties')
        props = portal_props.site_properties
        use_email_as_login = props.getProperty('use_email_as_login')

        # passwords should match
        if 'password' in form_field_names:
            assert('password_ctl' in form_field_names)
            # Skip this check if password fields already have an error
            if not ('password' in error_keys or \
                    'password_ctl' in error_keys):
                password = self.widgets['password'].getInputValue()
                password_ctl = self.widgets['password_ctl'].getInputValue()
                if password != password_ctl:
                    err_str = _(u'Passwords do not match.')
                    errors.append(WidgetInputError('password',
                                  u'label_password', err_str))
                    errors.append(WidgetInputError('password_ctl',
                                  u'label_password', err_str))
                    self.widgets['password'].error = err_str
                    self.widgets['password_ctl'].error = err_str

        # Password field checked against RegistrationTool
        if 'password' in form_field_names:
            # Skip this check if password fields already have an error
            if not 'password' in error_keys:
                password = self.widgets['password'].getInputValue()
                if password:
                    # Use PAS to test validity
                    err_str = registration.testPasswordValidity(password)
                    if err_str:
                        errors.append(WidgetInputError('password',
                                      u'label_password', err_str))
                        self.widgets['password'].error = err_str


        username = ''
#        email = ''
#        try:
#            email = self.widgets['email'].getInputValue()
#        except InputErrors, exc:
#            # WrongType?
#            errors.append(exc)
#        if use_email_as_login:
#            username_field = 'email'
#            username = email
#        else:
        username_field = 'username'
        try:
            username = self.widgets['username'].getInputValue()
        except InputErrors, exc:
            errors.append(exc)

        esd = self.context
        prefix = esd.prefix or esd.getId()
        prefix = str(prefix)
        username = "%s_%s" % (prefix, username)


        # check if username is valid
        # Skip this check if username was already in error list
        if not username_field in error_keys:
            if username == portal.getId():
                err_str = _(u"This username is reserved. Please choose a "
                            "different name.")
                errors.append(WidgetInputError(
                        username_field, u'label_username', err_str))
                self.widgets[username_field].error = err_str

        # check if username is allowed
        if not username_field in error_keys:
            if not registration.isMemberIdAllowed(username):
                err_str = _(u"The login name you selected is already in use "
                            "or is not valid. Please choose another.")
                errors.append(WidgetInputError(
                        username_field, u'label_username', err_str))
                self.widgets[username_field].error = err_str

        # Skip this check if email was already in error list
#        if not 'email' in error_keys:
#            if 'email' in form_field_names:
#                if not registration.isValidEmail(email):
#                    err_str = _(u'You must enter a valid email address.')
#                    errors.append(WidgetInputError(
#                            'email', u'label_email', err_str))
#                    self.widgets['email'].error = err_str

        if 'password' in form_field_names and not 'password' in error_keys:
            # Admin can either set a password or mail the user (or both).
            if not (self.widgets['password'].getInputValue() or
                    self.widgets['mail_me'].getInputValue()):
                err_str = _('msg_no_password_no_mail_me',
                            default=u"You must set a password or choose to "
                            "send an email.")
                errors.append(WidgetInputError(
                        'password', u'label_password', err_str))
                self.widgets['password'].error = err_str
                errors.append(WidgetInputError(
                        'mail_me', u'label_mail_me', err_str))
                self.widgets['mail_me'].error = err_str
        return errors
    
    @form.action(_(u'label_register', default=u'Register'),
                 validator='validate_registration', name=u'register')
    def action_join(self, action, data):
        # inject ESD
        esd = self.context
        prefix = esd.prefix or esd.getId()
        prefix = str(prefix)
        data['username'] = "%s_%s" % (prefix, data['username'])
        data['dp'] = esd.UID()
        data['groups'].append("%s_Members" % prefix)
        super(AddUserForm, self).handle_join_success(data)

        portal_groups = getToolByName(self.context, 'portal_groups')
        user_id = data['username']
        is_zope_manager = getSecurityManager().checkPermission(
            ManagePortal, self.context)

        try:
            # Add user to the selected group(s)
            if 'groups' in data.keys():
                for groupname in data['groups']:
                    group = portal_groups.getGroupById(groupname)
                    if 'Manager' in group.getRoles() and not is_zope_manager:
                        raise Forbidden
                    portal_groups.addPrincipalToGroup(user_id, groupname,
                                                      self.request)
        except (AttributeError, ValueError), err:
            IStatusMessage(self.request).addStatusMessage(err, type="error")
            return

        IStatusMessage(self.request).addStatusMessage(
            _(u"User added."), type='info')
        self.request.response.redirect(
            self.context.absolute_url() +
            '/@@usergroup-userprefs?searchstring=' + user_id)

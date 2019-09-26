# -*- coding: utf-8 -*-
from plone import api
from plone.app.textfield import RichTextValue
from plone.dexterity.events import EditFinishedEvent
from plone.namedfile.file import NamedBlobImage
from plone.protect.interfaces import IDisableCSRFProtection
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import get_installer
from Products.Five.browser import BrowserView
from zope.component import getUtility
from zope.event import notify
from zope.interface import alsoProvides
from zope.lifecycleevent import modified
from zope.schema.interfaces import IVocabularyFactory

import logging
import os

log = logging.getLogger(__name__)


def dummy_image(filename=u'image.png'):
    filename = os.path.join(os.path.dirname(__file__), filename)
    with open(filename, 'rb') as fd:
        data = fd.read()
    return NamedBlobImage(data=data, filename=filename)


class DocpoolSetup(BrowserView):
    """Setup some content useful for testing

    * Installs addons elan and doksys plus many dependencies
    * Create two docpools (b8nd and bayern)
    * Add a user tester:tester that can write into bund and read bayern
    * Create demo-content into bund/


    """

    def __call__(self):
        if not self.request.form.get('submit', None):
            return self.index()

        alsoProvides(self.request, IDisableCSRFProtection)

        # install addons
        installer = get_installer(self.context, self.request)
        installer.install_product('elan.policy')
        installer.install_product('docpool.doksys')
        installer.install_product('elan.journal')

        # TODO: pack bundles
        # @Steffen?

        # create docpool 1
        docpool_bund = api.content.create(
            container=self.context,
            type='DocumentPool',
            id='bund',
            title=u'Bund',
            prefix='bund',
            supportedApps=('elan', 'doksys'),
        )
        notify(EditFinishedEvent(docpool_bund))

        # create docpool 2
        docpool_land = api.content.create(
            container=self.context,
            type='DocumentPool',
            id='hessen',
            title=u'Hessen',
            prefix='hessen',
            supportedApps=('elan', 'doksys'),
        )
        notify(EditFinishedEvent(docpool_land))

        user1 = self.add_user(docpool_bund, 'user1', 'group1')
        user2 = self.add_user(docpool_land, 'user2', 'group2')

        # get the content-folder for a group to test with
        folder = docpool_bund['content']['Groups']['bund_group1']

        voc = getUtility(IVocabularyFactory, name='docpool.base.vocabularies.DocType')
        doctypes = voc(self.context).by_value
        doctypes_ids = [i.id for i in doctypes]

        # TODO a new event
        # folder = docpool_bund['content']['Groups']
        event_id = 'routinemode'

        # add one dpdocument for each type
        with api.env.adopt_user(user=user1):
            for doctype_id in doctypes_ids:
                new = api.content.create(
                    container=folder,
                    type='DPDocument',
                    title=u'{}'.format(doctype_id.capitalize()),
                    description=u'foo',
                    docType=doctype_id,
                    text=RichTextValue(u'<p>Body one</p>', 'text/html', 'text/x-html-safe'),
                    local_behaviors=['elan'],
                    scenarios=[event_id],
                )
                modified(new)
                api.content.create(
                    container=new,
                    type='Image',
                    title='{}_image'.format(doctype_id),
                    image=dummy_image()
                    )

                try:
                    api.content.transition(obj=new, transition='publish')
                except Exception as e:
                    log.info(e)
        return self.request.response.redirect(self.context.absolute_url())

    def add_user(self, docpool, username, groupname):
        """Create a User and a Group for a docpool for testing

        This is mimiking the code in docpool.users
        """
        gtool = getToolByName(docpool, 'portal_groups')
        docpool_uid = IUUID(docpool)
        docpool_title = docpool.Title()
        addname = groupname
        group_title = groupname
        description = ''
        prefix = docpool.prefix or docpool.id
        addname = "%s_%s" % (prefix, addname)
        group_title = '{} ({})'.format(group_title, docpool.Title())
        props = {
            'title': group_title,
            'description': 'A group to test with',
            'dp': docpool_uid,
        }
        # this uses the monkey-patched addGroup from docpool.users
        gtool.addGroup(
            addname,
            (),
            (),
            properties=props,
            title=group_title,
            description=description,
            REQUEST=self.request,
        )
        # it should create some content inside teh docpool. check for it:
        docpool.keys
        group1 = api.group.get(addname)

        # enable all doctypes for the new group
        voc = getUtility(IVocabularyFactory, name='docpool.base.vocabularies.DocType')
        doctypes = voc(docpool).by_value
        doctypes_ids = [i.id for i in doctypes]
        group1.setGroupProperties({'allowedDocTypes': doctypes_ids})
        # set docpool on group
        group1.setGroupProperties({'dp': docpool_uid})

        # add a user to test with
        user_fullname = '{} ({})'.format(username, docpool_title)
        user = api.user.create(
            email=u'tester@plone.org',
            username=username,
            password=username,
            roles=('Member',),
            properties={'fullname': user_fullname},
        )
        user.setMemberProperties(
            {'fullname': user_fullname, 'dp': docpool_uid}
        )
        api.group.add_user(group=group1, user=user)
        api.group.add_user(groupname='{}_DoksysUsers'.format(prefix), user=user)
        api.group.add_user(groupname='{}_ELANUsers'.format(prefix), user=user)
        return user

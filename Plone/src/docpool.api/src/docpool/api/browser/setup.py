# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.events import EditFinishedEvent
from plone.protect.interfaces import IDisableCSRFProtection
from Products.CMFPlone.utils import get_installer
from Products.Five.browser import BrowserView
from zope.component import getUtility
from zope.event import notify
from zope.interface import alsoProvides
from zope.lifecycleevent import modified
from zope.schema.interfaces import IVocabularyFactory
from plone.app.textfield import RichTextValue

import logging

log = logging.getLogger(__name__)


class DocpoolSetup(BrowserView):
    """Setup some content useful for testing

    * Installs addons elan and doksys plus many dependencies
    * Create two docpools (b8nd and bayern)
    * Add a user tester:tester that can write into bund and read bayern
    * Create demo-content into bund/


    """

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)

        # install addons
        installer = get_installer(self.context, self.request)
        installer.install_product('elan.policy')
        installer.install_product('docpool.doksys')
        installer.install_product('elan.journal')

        # TODO: pack bundles

        # create docpool 1
        docpool = api.content.create(
            container=self.context,
            type='DocumentPool',
            id='bund',
            title=u'Bund',
            supportedApps=('elan', 'doksys'),
        )
        notify(EditFinishedEvent(docpool))

        # create docpool 2
        docpool_2 = api.content.create(
            container=self.context,
            type='DocumentPool',
            id='bayern',
            title=u'Bayern',
            supportedApps=('elan', 'doksys'),
        )
        notify(EditFinishedEvent(docpool_2))

        # add a user to test with
        user = api.user.create(
            email=u'tester@plone.org',
            username=u'tester',
            password=u'tester',
            roles=('Member',),
            properties={'fullname': u'Tester'},
        )

        # add the user to the groups
        docpool_contentadmins = api.group.get('bund_ContentAdministrators')
        api.group.add_user(group=docpool_contentadmins, user=user)
        api.group.grant_roles(
            group=docpool_contentadmins,
            roles=['DocPoolUser', 'DoksysUser', 'ELANUser', 'Member', 'Reader'],
            )

        # enable all doctypes for this group
        voc = getUtility(IVocabularyFactory, name='docpool.base.vocabularies.DocType')
        doctypes = voc(self.context).by_value
        doctypes_ids = [i.id for i in doctypes]
        docpool_contentadmins.setGroupProperties({'allowedDocTypes': doctypes_ids})

        # get the content-folder for a group to test with
        groups = docpool['content']['Groups']
        folder = groups['bund_ContentAdministrators']

        # add dpdocuments of all types
        with api.env.adopt_user(user=user):
            for doctype_id in doctypes_ids:
                new = api.content.create(
                    container=folder,
                    type='DPDocument',
                    title=u'{}'.format(doctype_id.capitalize()),
                    description=u'foo',
                    docType=doctype_id,
                    text=RichTextValue(u'<p>Body one</p>', u'text/plain', u'text/html'),
                )
                modified(new)
                try:
                    api.content.transition(obj=new, transition='publish')
                except Exception as e:
                    log.info(e)
        return self.request.response.redirect(self.context.absolute_url())

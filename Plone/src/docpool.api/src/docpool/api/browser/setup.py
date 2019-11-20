# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
from plone import api
from plone.app.textfield import RichTextValue
from plone.dexterity.events import EditFinishedEvent
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from plone.protect.interfaces import IDisableCSRFProtection
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import get_installer
from Products.Five.browser import BrowserView
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.component import queryUtility
from zope.event import notify
from zope.interface import alsoProvides
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import modified
from zope.schema.interfaces import IVocabularyFactory
from zope.globalrequest import getRequest

import logging
import os
import random

log = logging.getLogger(__name__)


def dummy_image(filename=u'image.png'):
    filename = os.path.join(os.path.dirname(__file__), filename)
    with open(filename, 'rb') as fd:
        data = fd.read()
    return NamedBlobImage(data=data, filename=filename)


def dummy_file(filename=u'file.pdf'):
    filename = os.path.join(os.path.dirname(__file__), filename)
    with open(filename, 'rb') as fd:
        data = fd.read()
    return NamedBlobFile(data=data, filename=filename)


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
        log.info(u'Created docpool bund')

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
        log.info(u'Created docpool hessen')

        user1 = add_user(docpool_bund, 'user1', ['group1'])
        log.info(u'Created user1 and group1 in docpool bund')
        user2 = add_user(docpool_land, 'user2', ['group2'])
        log.info(u'Created user2 and group2 in docpool hessen')

        # get the content-folder for a group to test with
        folder = docpool_bund['content']['Groups']['bund_group1']

        voc = getUtility(IVocabularyFactory, name='docpool.base.vocabularies.DocType')
        doctypes = voc(self.context).by_value
        doctypes_ids = [i.id for i in doctypes]

        event_id = 'routinemode'

        even_config_folder = docpool_bund['contentconfig']['scen']
        dpnuclearpowerstation = api.content.create(
            container=even_config_folder,
            type='DPNuclearPowerStation',
            id='kernkraftwerk-1',
            title=u'Kernkraftwerk 1',
            coordinates=u'POINT(12.240313700000002 48.59873489999998)',
            )
        log.info(u'Created dpnuclearpowerstation')
        dpnetwork = api.content.create(
            container=even_config_folder,
            type='DPNetwork',
            id='testnetz',
            title=u'Testnetz',
            coordinates=u'POLYGON((12.789515693194565 48.70897536061274,11.9394485546417 48.750643880797945,11.725215156233618 48.447309003359074,12.352809150286648 48.38076862235553,12.803248603348985 48.39080082760333,12.789515693194565 48.70897536061274))',
            )
        log.info(u'Created dpnetwork')
        dpevent = api.content.create(
            container=even_config_folder,
            type='DPEvent',
            id='test-event',
            title=u'Test Event',
            description=u'Die Beschreibung',
            Status='active',
            AlertingStatus=u'none',
            AreaOfInterest=u'POLYGON((12.124842841725044 48.60077830054228,12.157801826095657 48.51533914735478,12.702998359223052 48.63164629148582,12.865046699043434 48.77393903963252,12.124842841725044 48.60077830054228))',
            EventCoordinates=u'POINT(12.240313700000002 48.59873489999998)',
            EventLocation=RelationValue(get_intid(dpnuclearpowerstation)),
            SectorizingNetworks=[RelationValue(get_intid(dpnetwork))],
            EventPhase=None,
            Exercise=True,
            TimeOfEvent=datetime.now(),
            OperationMode='routine',
            SectorizingSampleTypes=[u'A', u'A1', u'A11', u'A12', u'A13', u'A2', u'A21', u'A22', u'A23', u'A24', u'A3', u'A31', u'A32', u'B11'],
            )
        log.info(u'Created dpevent')

        # TODO:
        # Add SRModuleTypes
        # Add lagebericht-konfiguration
        # Add szenario
        # Add phase
        # Add modulkonfiguration

        with api.env.adopt_user(user=user1):
            sampletype_ids = [u'9', u'A', u'B', u'F', u'G', u'I', u'L', u'M', u'N', u'S', u'Z']
            # add one dpdocument for each type
            for doctype_id in doctypes_ids:
                new = api.content.create(
                    container=folder,
                    type='DPDocument',
                    title=u'{}'.format(doctype_id.capitalize()),
                    description=u'foo',
                    docType=doctype_id,
                    text=RichTextValue(u'<p>Text</p>', 'text/html', 'text/x-html-safe'),
                    local_behaviors=['elan', 'doksys'],
                    scenarios=[dpevent.id],
                    SampleTypeId=random.choice(sampletype_ids),
                    Area=u'D',
                    DataType=u'ONMON',
                    Dom=u'84 _deposition_ground_beta surface activity_2 h',
                    Duration=u'1d',
                    LegalBase=u'IRMIS',
                    MeasurementCategory=u'Si-31',
                    MeasuringProgram=u'Intensivmessprogramm',
                    NetworkOperator=u'Bremen',
                    OperationMode=u'Routine',
                    Purpose=u'Standard-Info Bundesmessnetze',
                    SampleType=u'Kompost',
                    SamplingBegin=datetime.now(),
                    SamplingEnd=datetime.now() + timedelta(hours=1),
                    Status=u'geprueft',
                    TrajectoryEndTime=datetime.now() + timedelta(hours=1),
                    TrajectoryStartTime=datetime.now(),
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
                log.info(u'Created dpdocument of type {}'.format(doctype_id))

            # add one full DPDocument
            new = api.content.create(
                container=folder,
                type='DPDocument',
                title=u'Eine Bodenprobe',
                description=u'foo',
                text=RichTextValue(u'<p>Bodenprobe!</p>', 'text/html', 'text/x-html-safe'),
                docType='groundcontamination',
                scenarios=[dpevent.id],
                local_behaviors=['elan', 'doksys'],
                Area=u'D',
                DataType=u'ONMON',
                Dom=u'84 _deposition_ground_beta surface activity_2 h',
                Duration=u'1d',
                LegalBase=u'IRMIS',
                MeasurementCategory=u'Si-31',
                MeasuringProgram=u'Intensivmessprogramm',
                NetworkOperator=u'Bremen',
                OperationMode=u'Routine',
                Purpose=u'Standard-Info Bundesmessnetze',
                SampleType=u'Kompost',
                SampleTypeId=u'B2',
                SamplingBegin=datetime.now(),
                SamplingEnd=datetime.now() + timedelta(hours=1),
                Status=u'geprueft',
                TrajectoryEndTime=datetime.now() + timedelta(hours=1),
                TrajectoryStartTime=datetime.now(),
            )
            modified(new)
            api.content.create(
                container=new,
                type='Image',
                title=u'Ein Bild',
                image=dummy_image(),
                )
            api.content.create(
                container=new,
                type='File',
                title=u'Eine Datei',
                file=dummy_file(),
                )
            api.content.transition(obj=new, transition='publish')
            log.info(u'Created dpdocument Eine Bodenprobe {}'.format(
                new.absolute_url()))

        return self.request.response.redirect(self.context.absolute_url())


def add_user(
       docpool,
       username,
       groupnames=None,
       enabled_apps=['elan', 'doksys'],
       ):
    """Create a User and a Group for a docpool for testing.

    This mimicks adding groups in the application in docpool.users by:
    * adding the docpool-prefix to the groups id and title
    * allowing all doctypes
    * assigning the docpool

    """
    docpool_title = docpool.Title()
    prefix = docpool.prefix or docpool.id
    docpool_uid = IUUID(docpool)
    groupnames = groupnames if groupnames else []
    for groupname in groupnames:
        add_group(docpool, groupname)

    # add the user
    user_fullname = '{} ({})'.format(username, docpool_title)
    user = api.user.create(
        email=u'tester@plone.org',
        username=username,
        password=username,
        roles=('Member',),
        properties={'fullname': user_fullname},
    )
    user.setMemberProperties(
        {
            'fullname': user_fullname,
            'dp': docpool_uid,
            'apps': enabled_apps,
        }
    )
    # add the user to specified groups
    for groupname in groupnames:
        real_groupname = '%s_%s' % (prefix, groupname)
        group = api.group.get(real_groupname)
        api.group.add_user(group=group, user=user)

    api.group.add_user(groupname='{}_Members'.format(prefix), user=user)
    if 'doksys' in enabled_apps:
        api.group.add_user(groupname='{}_DoksysUsers'.format(prefix), user=user)
    if 'elan' in enabled_apps:
        api.group.add_user(groupname='{}_ELANUsers'.format(prefix), user=user)
    pm = getToolByName(docpool, 'portal_membership')
    pm.createMemberArea(username)
    return user


def add_group(docpool, groupname):
    """Add a group in a docpool.

    This mimicks adding groups in the application by:
    * adding the docpool-prefix to the groups id and title
    * put all doctypes in memberdata to allow creating all DPDocuments
    * put docpool-id in memberdata
    """
    # get all doctypes to enable them for the new group
    voc = getUtility(IVocabularyFactory, name='docpool.base.vocabularies.DocType')
    doctypes = voc(docpool).by_value
    doctypes_ids = [i.id for i in doctypes]

    gtool = getToolByName(docpool, 'portal_groups')
    docpool_uid = IUUID(docpool)
    docpool_title = docpool.Title()
    group_title = '{} ({})'.format(groupname.capitalize(), docpool_title)
    description = ''
    prefix = docpool.prefix or docpool.id
    groupname = '%s_%s' % (prefix, groupname)

    if api.group.get(groupname=groupname) is not None:
        log.info(u'Skipping. Group {} exists.'.format(groupname))
        return

    props = {
        'title': group_title,
        'description': description,
        'dp': docpool_uid,
        'allowedDocTypes': doctypes_ids,
    }
    request = getRequest()
    if request.method != 'POST':
        # fool addGroup to allow to work even without a real POST
        request.method = 'POST'
    # this uses the monkey-patched addGroup from docpool.users
    # it will create a group-folder inside the docpool
    gtool.addGroup(
        id=groupname,
        roles=(),
        groups=(),
        properties=props,
        REQUEST=request,
        title=group_title,
        description=description,
    )
    return api.group.get(groupname)


def get_intid(obj):
    """Intid from intid-catalog"""
    intids = queryUtility(IIntIds)
    if intids is None:
        return
    # check that the object has an intid, otherwise there's nothing to be done
    try:
        return intids.getId(obj)
    except KeyError:  # noqa
        # The object has not been added to the ZODB yet
        return

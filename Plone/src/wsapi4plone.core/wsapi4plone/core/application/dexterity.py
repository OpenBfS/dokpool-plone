from DateTime import DateTime
from plone.app.textfield import RichText
from plone.behavior.interfaces import IBehaviorAssignable
from plone.dexterity.interfaces import IDexterityContent, IDexterityContainer
from plone.namedfile.file import NamedBlobImage, NamedBlobFile
from Products.CMFPlone.utils import safe_unicode
from six.moves.xmlrpc_client import DateTime as XMLRPCDateTime
from wsapi4plone.core.application.services import PloneService
from wsapi4plone.core.application.services import PloneServiceContainer
from wsapi4plone.core.interfaces import IServiceContainer
from z3c.relationfield.relation import RelationValue
from z3c.relationfield.schema import RelationList, RelationChoice
from zope.component import adapter
from zope.interface import implementer_only
from zope.schema import getFieldsInOrder

import logging
import six
import six.moves.xmlrpc_client

logger = logging.getLogger("WSA API USER")


@adapter(IDexterityContent)
class DexterityObjectService(PloneService):

    def get_object(self, attrs=[]):
        skeleton = self.get_skeleton(attrs, just_keys=True)
        skeleton['id'] = None
        if not skeleton:
            return None
        for k in skeleton.keys():
            if hasattr(self.context, k):
                v = getattr(self.context, k)
                if isinstance(v, RelationValue):
                    v = v.to_path
                elif callable(v):
                    v = v()
                if isinstance(v, DateTime):
                    v = XMLRPCDateTime(v)
                skeleton[k] = v
        # print skeleton
        return skeleton

    def _fields(self):
        """
        """
        context = self.context
        behavior_fields = []

        # Stap 1 metadata
        behavior_assignable = IBehaviorAssignable(context)
        if behavior_assignable:
            behaviors = behavior_assignable.enumerateBehaviors()
            for behavior in behaviors:
                behavior_fields += getFieldsInOrder(behavior.interface)

        # Stap 2 eigen velden
        fti = context.getTypeInfo()
        schema = fti.lookupSchema()
        content_fields = getFieldsInOrder(schema)
        fields = behavior_fields
        fields += content_fields

        #        for field_info in fields:
        #            try:
        #                field_name = field_info[0]
        #                field = field_info[1]
        #                print field_info
        #                print getattr(context, field_name)
        #            except Exception, e:
        #                pass

        return fields

    def get_skeleton(self, filtr=[], *args, **kwargs):
        """
        @param filtr - list of attribute names that will make up the skeleton
        @kwarg just_keys - (boolean) - returns only the keys and the value as None
        """

        fields = self._fields()
        if not filtr:
            filtr = [f[0] for f in fields]
        skeleton = {}
        for field in fields:
            name = field[0]
            if name in filtr:
                # TODO pumazi: include default data and ...
                # if it is a selection, boolean, etc., provide values that are
                # acceptable.
                if kwargs.get('just_keys'):
                    skeleton[name] = None
                else:
                    skeleton[name] = {
                        'type': field[1], 'required': field[1].required}
        return dict(skeleton)

    def set_properties(self, params):
        for par in params:
            if isinstance(params[par], six.moves.xmlrpc_client.DateTime):
                params[par] = DateTime(
                    params[par].value).asdatetime().replace(tzinfo=None)
            elif isinstance(params[par], six.moves.xmlrpc_client.Binary):
                # import pdb; pdb.set_trace()
                params[par] = params[par].data
            elif par == 'creators':
                params[par] = tuple(params[par])
            elif isinstance(params[par], str) and par != 'id':
                # print "set_properties", par
                params[par] = six.text_type(params[par])
            # elif isinstance(self.context[attr], BaseUnit):
            #     self.context[par].update(params[par], self.context[par])
            #     del params[par]
        context = self.context
        changed = []

        behavior_fields = []
        content_fields = []

        # Step 1 metadata

        # Fake a form submit, so that local behaviors are not evaluated
        request = self.context.REQUEST
        request.set("form.buttons.save", True)

        behavior_assignable = IBehaviorAssignable(context)
        if behavior_assignable:
            behaviors = behavior_assignable.enumerateBehaviors()
            # print behaviors
            for behavior in behaviors:
                # print getFieldsInOrder(behavior.interface)
                behavior_fields += getFieldsInOrder(behavior.interface)

        # Stap 2 eigen velden
        fti = context.getTypeInfo()
        schema = fti.lookupSchema()
        content_fields = getFieldsInOrder(schema)

        fields = behavior_fields
        fields += content_fields

        for k, v in params.items():
            found = False
            # print k, v
            for field_info in fields:
                try:
                    field_name = field_info[0]
                    field = field_info[1]
                    field_schema = getattr(field, 'schema', None)
                    # print field_name, field_schema, field_schema and field_schema.getName()
                    if field_name == k:
                        if field_schema and field_schema.getName() in [
                            'INamedBlobImage',
                            'INamedBlobFile',
                        ]:
                            found = True
                            filename = ''
                            # print type(v)
                            if isinstance(v, type(())):
                                # print "mod"
                                filename = safe_unicode(v[1])
                                v = v[0].data
                            # print len(v), filename
                            if field_schema.getName() == 'INamedBlobImage':
                                v = NamedBlobImage(data=v, filename=filename)
                            elif field_schema.getName() == 'INamedBlobFile':
                                v = NamedBlobFile(data=v, filename=filename)
                            setattr(context, field_name, v)
                            changed.append(k)

                        elif isinstance(field, RelationChoice):
                            if type(v) in [list, tuple]:
                                v = v[0]
                            context.set_relation(field_name, path=v)

                        elif isinstance(field, RelationList):
                            value = v
                            if type(value) in [str, six.text_type]:
                                value = [value]
                            context.set_relation(field_name, paths=value)
                        elif isinstance(field, RichText):
                            setattr(context, field_name, field.fromUnicode(v))
                        elif field_name == 'subjects':
                            setattr(context, 'subject', v)
                        else:
                            found = True
                            field.set(context, v)
                            changed.append(k)
                        logger.info(u'Setting field "{0}"'.format(k))
                except Exception as e:
                    logger.exception(
                        "Error with field '{0}'  : {1}".format(field_name, e)
                    )
                    pass

            if not found:
                logger.warn(u'Cannot find field "{0}"'.format(k))

        if changed:
            context.reindexObject(idxs=changed)


@implementer_only(IServiceContainer)
@adapter(IDexterityContainer)
class DexterityContainerService(PloneServiceContainer, DexterityObjectService):
    pass

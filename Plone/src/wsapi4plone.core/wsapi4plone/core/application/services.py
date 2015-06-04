# -*- coding: utf-8 -*-
"""Core services that work with Plone out-of-the-box"""
import datetime
import time
import xmlrpclib

from DateTime import DateTime
from OFS.Image import File, Pdata
from zope.component import adapts, getUtility
from zope.interface import implements, implementsOnly
from zope.publisher.interfaces import NotFound

from Products.Archetypes.BaseUnit import BaseUnit
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
try:
    from plone.app.blob.interfaces import IBlobWrapper
    has_blob_support = True
except ImportError:
    has_blob_support = False

from wsapi4plone.core.interfaces import IServiceContainer, IFormatQueryResults
from wsapi4plone.core.service import Service, ServiceContainer


class PloneService(Service):
    # implements(IService)

    def _gather_file_data(self, attr):
        broken_bones = self.context[attr]._properties
        mended_bones = {}
        # mend the broken bones into a shape they can be
        # surgically implanted into the skeleton
        for p in broken_bones:
            attr_id = p['id']
            # Assemble the bones into an unbroken order
            mended_bones[attr_id] = dict([ (x, p[x]) for x in p if x != 'id' ])
        # Mend the bones with data
        for k in mended_bones:
            if hasattr(self.context[attr], k):
                bone_marrow = getattr(self.context[attr], k)
                if callable(bone_marrow):
                    try:
                        mended_bones[k] = bone_marrow()
                    except:
                        # ignore
                        pass
                else:
                    mended_bones[k] = bone_marrow
            else:
                mended_bones[k] = None
        # Wrap it up with the data
        # I am assuming all 'File' objects have the data and size attributes
        #   that have the file's data and size, respectfully.
        if isinstance(self.context[attr].data, Pdata):
            # need to get the string of this otherwise we get an ImplicitAcquirerWrapper.
            mended_bones['data'] = xmlrpclib.Binary(str(self.context[attr].data))
        else:
            mended_bones['data'] = xmlrpclib.Binary(self.context[attr].data)
        mended_bones['size'] = self.context[attr].size
        return mended_bones

    def _gather_blob_data(self, attr):
        blob = self.context[attr]
        gathered_data = {'content_type': blob.content_type,
                         'data': xmlrpclib.Binary(blob.data),
                         'size': blob.size(),
                         }
        if hasattr(blob, 'title') and blob.title is not None:
            gathered_data['title'] = blob.title
        if hasattr(blob, 'width'):
            gathered_data['width'] = blob.width
            gathered_data['height'] = blob.height
        return gathered_data

    def get_skeleton(self, filtr=[], *args, **kwargs):
        """
        @param filtr - list of attribute names that will make up the skeleton
        @kwarg just_keys - (boolean) - returns only the keys and the value as None
        """
        # this should be type agnostic (Archtypes, zope3 schemas, ZClasses, etc.)
        # built for archtypes atm
        if hasattr(self.context, 'Schema'):
            # the belief is that all AT objects will have a schema attribute
            schema = self.context.Schema()
        else:
            # do something with non-AT objects
            # get dictionary form of the schema
            return # for the time being... no object also comes here

        fields = schema.values()
        if not filtr: filtr = schema.keys()
        skeleton = {}
        for field in fields:
            name = field.getName()
            if name in filtr:
                # TODO pumazi: include default data and ...
                # if it is a selection, boolean, etc., provide values that are acceptable.
                if kwargs.get('just_keys'):
                    skeleton[name] = None
                else:
                    skeleton[name] = {'type': field.type, 'required': field.required}
        return dict(skeleton)

    def get_object(self, attrs=[]):
        skeleton = self.get_skeleton(attrs, just_keys=True)
        print self.context
        print skeleton
        if not skeleton:
            return None
        for k in skeleton.keys():
            if self.context.get(k, None) == None:
                skeleton[k] = None
            elif isinstance(self.context[k], BaseUnit):
                # -- it's worse than the x-ray shows --
                # brittle_bones, tisk tisk
                # 
                # Archetypes' BaseUnit subclasses OFS's File, which has the
                # _properties attribute, but it loses its 'id' and
                # 'content_type' ???
                skeleton[k] = self.context[k].getRaw()
            elif isinstance(self.context[k], File):
                skeleton[k] = self._gather_file_data(k)
            elif has_blob_support and IBlobWrapper.providedBy(self.context[k]):
                skeleton[k] = self._gather_blob_data(k)
            else:
                skeleton[k] = self.context[k]
        return skeleton

    def get_type(self):
        return self.context.getTypeInfo().id

    def set_properties(self, params):
        for par in params:
            if isinstance(params[par], xmlrpclib.DateTime):
                params[par] = DateTime(params[par].value)
            elif isinstance(params[par], xmlrpclib.Binary):
                params[par] = params[par].data
            # elif isinstance(self.context[attr], BaseUnit):
            #     self.context[par].update(params[par], self.context[par])
            #     del params[par]
        self.context.update(**params)


class PloneServiceContainer(PloneService, ServiceContainer):
    implementsOnly(IServiceContainer)

    def create_object(self, type_name, id_):
        new_id = self.context.invokeFactory(type_name=type_name, id=id_)
        assert new_id == id_, "New id (%s) does not equal the excepted id (%s)." % (new_id, posted_id)
        return id_

    def delete_object(self, id_):
        try:
            self.context.manage_delObjects(id_)
        except AttributeError, e:
            raise NotFound(self.context, id_, '%s does not exist' % id_)

        if getattr(self.context, id_, None):
            return False
        else:
            return True


class PloneRootService(PloneServiceContainer):
    """Adapts a Plone Site object"""
    adapts(IPloneSiteRoot)
    # implements(IServiceContainer)

    def get_skeleton(self, filtr=[], *args, **kwargs):
        return {'id': {'required': True, 'type': 'string'},
                'title': {'required': True, 'type': 'string'},
                'description': {'required': False, 'type': 'string'}}

# -*- coding: utf-8 -*-
from docpool.dbaccess.dbinit import __metadata__, __session__
from docpool.dbaccess.content.registry import registerEntityConfig
from formalchemy.fields import HiddenFieldRenderer
from docpool.dbaccess.content.forms import NoRenderer
from operator import attrgetter

metadata = __metadata__
session = __session__

from elixir import *
from sqlalchemy.orm import class_mapper
from formalchemy import FieldSet, Grid, Field
from formalchemy import types
from sqlalchemy.orm.properties import RelationProperty
from docpool.dbaccess import DocpoolMessageFactory as _


class StructuredEntity(object):

    _c_min_ = 0
    _c_max_ = 0

    @classmethod
    def mandatory(cls):
        """
        """
        return cls._c_min_ == 1

    @classmethod
    def single(cls):
        """
        """
        return cls._c_max_ == 1

    @classmethod
    def multiple(cls):
        """
        """
        return cls._c_max_ > 1

    @classmethod
    def max(cls):
        """
        """
        return cls._c_max_

    @classmethod
    def fkName(cls):
        """
        Name of the foreign key used to reference instances from subentities
        """
        return cls.__name__ + "_id"

    @classmethod
    def typename(cls):
        """
        """
        return cls.__name__.lower()

    @classmethod
    def fields(cls):
        """
        """
        cm = class_mapper(cls)
        if cm:
            fields = [
                f for f in cm.columns.keys() if not (f.find("_id") > 0 or f == "id")
            ]
            # print cm.columns
            for f in cm.primary_key:
                # print f
                if f.name in fields:
                    fields.remove(f.name)
            return fields
        else:
            return []

    @classmethod
    def fieldset(cls):
        """
        Generic FieldSet generation.
        """
        fields = cls.fields()
        fs = FieldSet(cls, session=__session__)
        if hasattr(cls, "myfieldsetconfig"):
            fsconfig = cls.myfieldsetconfig(fs)
            fs.configure(include=fsconfig)
        else:
            fs.configure(include=[getattr(fs, fname) for fname in fields])
        return fs

    @classmethod
    def grid(cls):
        """
        """
        fields = cls.fields()
        g = Grid(cls, session=__session__)
        if hasattr(cls, "mygridconfig"):
            gconfig = cls.mygridconfig(g)
        else:
            gconfig = [getattr(g, fname) for fname in fields]
        if gconfig:
            g.configure(include=gconfig, readonly=True)
        #            g.insert(g[fields[0]], Field('check', type=types.String, value=lambda item: "<input type='checkbox' name='objsel:list' value=\"%s\"/>" % (str(item._sa_instance_state.key[1]))))
        else:
            g.configure(readonly=True)
        return g

    @classmethod
    def create_fs(cls, context):
        """
        """
        fs = cls.fieldset()
        se = cls.superentity()
        if se:
            fk = se.fkName()
            fs.append(fs[fk].with_renderer(NoRenderer))
        return fs

    @classmethod
    def edit_fs(cls, context):
        """
        """
        return cls.fieldset()

    @classmethod
    def filter_fs(cls, context):
        """
        """
        return cls.fieldset()

    @classmethod
    def list_fs(cls, context):
        """
        """
        g = cls.grid()
        g.append(
            Field(
                'editlink',
                type=types.String,
                value=lambda item: "<a href=\"%s/struct_edit?typ=%s&pk=%s&bc=%s\">"
                % (
                    context.getContextObj().absolute_url(),
                    cls.typename(),
                    str(item._sa_instance_state.key[1]),
                    context.getView().parentView.breadcrumbs(),
                )
                + _("Edit")
                + "</a>",
            )
        )
        return {'form': g, 'importRestricted': True, 'sortNames': []}

    @classmethod
    def subentities(cls):
        """
        should be overridden in subclasses if ordering is required
        """
        cm = class_mapper(cls)
        entities = []
        for r in cm._props._list:
            if type(cm._props[r]) == RelationProperty:
                p = cm._props[r]
                if p.uselist:
                    entities.append(p.mapper.class_)
        entities.sort(key=attrgetter('__name__'))
        return entities

    @classmethod
    def superentity(cls):
        cm = class_mapper(cls)
        for r in cm._props._list:
            if type(cm._props[r]) == RelationProperty:
                p = cm._props[r]
                if not p.uselist:
                    return p.mapper.class_
        return None

    @classmethod
    def structure(cls):
        return getStructure(cls)

    @classmethod
    def register(cls):
        registerEntityConfig(
            cls.typename(),
            cls,
            gen_fs=True,
            protect=True,
            list_fs=cls.list_fs,
            edit_fs=cls.edit_fs,
            create_fs=cls.create_fs,
            sort_default='id',
            label=_(cls.__name__),
        )

    def getPrimaryKeyValue(self):
        return self.id

    def getSubObjects(self, bc=[]):
        cls = self.__class__
        fkName = cls.fkName()
        typ = cls.typename()
        pk = self.getPrimaryKeyValue()
        ses = cls.subentities()
        kwargs = {fkName: pk}
        subres = []
        mybc = bc[:]
        mybc.append((typ, [pk]))
        for se in ses:
            subobjects = __session__.query(se).filter_by(**kwargs).all()
            for so in subobjects:
                subres.append(so.getSubObjects(mybc))

        return (self.__repr__(), typ, str([pk]), str(bc), subres)

    def __repr__(self):
        return self.__class__.__name__ + " " + str(self.id)


def getStructure(cls):
    """
    """
    mandatory = cls.mandatory()
    single = cls.single()
    multiple = cls.multiple()
    fields = cls.fields()
    max = cls.max()
    e = {
        'entity': cls,
        'fields': fields,
        'mandatory': mandatory,
        'single': single,
        'multiple': multiple,
        'max': max,
        'subentities': [],
    }
    for se_cls in cls.subentities():
        e['subentities'].append(getStructure(se_cls))
    return e

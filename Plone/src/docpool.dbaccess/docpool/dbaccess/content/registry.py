# -*- coding: utf-8 -*-

__author__ = 'Condat AG'
__docformat__ = 'plaintext'

from elixir import setup_all
from docpool.dbaccess.dbinit import __session__, __metadata__
from sqlalchemy.orm import class_mapper
from Products.CMFPlone.log import log_exc

# Kompatibilitaet fuer SQLAlchemy > 0.6
try:
    from sqlalchemy.orm import RelationProperty
except ImportError:
    from sqlalchemy.orm.properties import RelationProperty
from formalchemy import FieldSet, Grid
from formalchemy import Field
from formalchemy import types

_ecreg = {}  # Laufzeit Registry

# TODO: Export Config
_exportConfigReg = {}
_reportConfigReg = {}


def getAllEntityFields(klass):
    """
    """
    cm = class_mapper(klass)  # SA Mapper dieser Klasse holen
    if cm:
        fields = cm.columns.keys()  # Spalten lesen
        for f in cm.primary_key:  # Primaerschluesselfelder nicht
            if f.name in fields:
                fields.remove(f.name)
        for r in cm._props.keys():
            if type(cm._props[r]) == RelationProperty:  # Relationen zufuegen
                fields.append(r)
        return fields
    else:
        return []


def _makeFS(klass, fields):
    """
    Erzeugt aus einer Feldliste und einer Pythonklasse ein Fieldset fuer alle Felder.
    """
    # print fields
    fs = FieldSet(klass, session=__session__)
    fs.configure(include=[getattr(fs, fname) for fname in fields])
    return fs


def _makeGrid(typ, klass, fields):
    """
    Erzeugt aus einer Feldliste und einer Pythonklasse ein Grid fuer alle Felder.
    """
    #    print fields
    first_field = fields[0]
    #    print first_field

    g = Grid(klass, session=__session__)
    g.configure(include=[getattr(g, fname) for fname in fields], readonly=True)
    g.append(
        Field(
            'editlink',
            type=types.String,
            value=lambda item: "<a href=\"portal_dbadmin/objekt_edit?typ=%s&pk=%s\">Editieren</a>"
            % (typ, str(item._sa_instance_state.key[1])),
        )
    )
    #    print getattr(g, first_field)
    g.insert(
        getattr(g, first_field),
        Field(
            'check',
            type=types.String,
            value=lambda item: "<input type='checkbox' name='objsel:list' value=\"%s\"/>"
            % (str(item._sa_instance_state.key[1])),
        ),
    )
    return g


def registerEntityConfig(
    typ,
    klass,
    gen_fs=False,
    protect=False,
    edit_fs=None,
    create_fs=None,
    list_fs=None,
    filter_fs=None,
    sort_default=None,
    label=None,
):
    """
    Erlaubt das programmatische Definieren oder Ueberschreiben von Entity Konfigurationen.
    D.h. statt eines EntityConfig Objekts wird eine interne Registry genutzt, 
    um alle Aspekte der Darstellung persistent abzulegen.
    Wenn 'protect' = True, dann werden die Eintraege durch einen erneuten Aufruf nicht ueberschrieben -
        es sei denn, der erneute Aufruf spezifiziert wieder 'protect' = True.
    Wenn andere Parameter None sind und gen_fs == False, dann bleiben etwaige vorherige Eintraege erhalten. So kann man gezielt auch
    Teile ueberschreiben.  Ist gen_fs == True, werden generisch Defaults fuer fehlende Parameter erzeugt.
    """
    # print "**************** registerEntityConfig", typ, gen_fs, protect
    if not label:
        label = typ.capitalize()

    econfig = {}
    if _ecreg.has_key(typ):
        econfig = _ecreg[typ]
        if (
            econfig['protect'] and not protect
        ):  # Eintrag ist geschuetzt und wird nicht ueberschrieben
            # print "PROTECTED"
            return
    econfig['label'] = label
    econfig['klass'] = klass
    econfig['protect'] = protect

    if gen_fs:
        try:
            fields = getAllEntityFields(klass)

            if not edit_fs:
                edit_fs = _makeFS(klass, fields)
            if not create_fs:
                create_fs = _makeFS(klass, fields)
            if not list_fs:
                list_fs = _makeGrid(typ, klass, fields)
            if not filter_fs:
                filter_fs = _makeFS(klass, fields)
            if not sort_default:
                sort_default = fields[0]
        except "Exception, e":  # Bei ungewoehnlichen (binaeren) Feldern
            log_exc(e)

    if edit_fs:
        econfig['edit_def'] = edit_fs
    if create_fs:
        econfig['create_def'] = create_fs
    if list_fs:
        econfig['list_def'] = list_fs
    if filter_fs:
        econfig['filter_def'] = filter_fs
    if sort_default:
        econfig['sort_default'] = sort_default

    # print "Registering...", typ, econfig
    _ecreg[typ] = econfig


def unregisterEntityConfig(typ):
    """
    """
    if _ecreg.has_key(typ):
        del _ecreg[typ]


def unregisterExportDBObjectConfig(typ):
    """
    """
    if _exportConfigReg.has_key(typ):
        del _exportConfigReg[typ]


def registerExportDBObjectConfig(
    typ,
    klass,
    felder,
    zusatzFelder=None,
    methodeFuerZusatzFelder=None,
    name='Standard',
    encoding=None,
):
    """
    @param typ: Registrierte Entitykonfiguration
    @param klass: OR-Klasse/ ggf. Entity-Klasse
    @param felder: Liste an Bezeichnern der DB-Felder, die exportiert werden sollen ggf. Angabe von Dummyfeldern mit Vorbelegung.
                   <Feldname> oder <Feldname/ Attribut>:<Datentyp (int, bool, date)> oder <Relationsname>|<Entity>|<Feldname/ Attribut>
                   oder <Dummyfeldname>#<Dummywert>
    @param zusatzFelder: Optional: Bezeichnung der Spalten, die hinten an die in der Liste "felder" bezeichneten Spalten angehaengt werden.
    @param methodeFuerZusatzFelder: Bestimmung der Werte fuer die Zusatzfelder mit einer optional anzugebenden Methode.
    @param name: Damit koennen ggf. mehrere Exportdefinitionen registriert werden.
    """
    exConfig = {}
    exConfig['klass'] = klass
    exConfig['felder'] = felder
    exConfig['zusatzFelder'] = zusatzFelder
    exConfig['methodeFuerZusatzFelder'] = methodeFuerZusatzFelder
    exConfig['encoding'] = encoding
    if _exportConfigReg.has_key(typ):
        _exportConfigReg[typ].append((name, exConfig))
    else:
        _exportConfigReg[typ] = [(name, exConfig)]


def registerReportConfig(typ, klass, reportTemplateName, name='Standard'):
    """
    """
    reportConfig = {'klass': klass, 'reportTemplateName': reportTemplateName}
    # TODO: nicht doppelt registriern!
    if _reportConfigReg.has_key(typ):
        _reportConfigReg[typ].append((name, reportConfig))
    else:
        _reportConfigReg[typ] = [(name, reportConfig)]


def bootstrapRegistry():
    """
    Bestimmt die im System vorhandenen Entities und registriert diese.
    Die Entities werden ueber die SA Mapper bestimmt.
    """
    # print "dbadmin: Bootstrapping..."
    # Wir holen uns alle Mapper
    from sqlalchemy.orm import _mapper_registry

    for mapper in _mapper_registry.keys():
        klass = mapper.class_
        typ = klass.__name__
        registerEntityConfig(typ.lower(), klass, gen_fs=True)
    # pprint(_ecreg)


setup_all()
# bootstrapRegistry() # Minimale Initialisierung mit dem, was halt schon da ist...
# Diese feste generische Registierung wollen wir nicht. Das kann bei einzelnen Installationen
# in kundenspezifischen Produkten aufgerufen werden. Aber generell sollen alle Entities explizit registriert werden.

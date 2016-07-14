# -*- coding: utf-8 -*-
#
# File: dbadmin.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#
from Products.PageTemplates.tests.batch import __allow_access_to_unprotected_subobjects__

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the dbadmin content type. See dbadmin.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from zope.component import adapts

from Products.Archetypes.interfaces import IObjectPostValidation

try:
    from Products.LinguaPlone import public as atapi
except ImportError:
    # No multilingual support
    from Products.Archetypes import atapi

from Products.ATContentTypes.content import base

from docpool.dbaccess.interfaces import Idbadmin
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.CMFCore.utils import getToolByName


##code-section imports
from docpool.dbaccess.dbinit import __session__, __metadata__
metadata = __metadata__
session = __session__

from elixir import *
from sqlalchemy import or_, and_, join, asc, desc, func
from sqlalchemy.orm import class_mapper, ColumnProperty
# Kompatibilitaet fuer SQLAlchemy > 0.6
try:
    from sqlalchemy.orm import RelationProperty
except ImportError:
    from sqlalchemy.orm.properties import RelationProperty

from formalchemy import FieldSet, Grid
from formalchemy import config
from formalchemy import types
from formalchemy import Field
from formalchemy import FieldRenderer
import sys
import forms
import imports
from registry import _ecreg, registerEntityConfig,\
                     _exportConfigReg, registerExportDBObjectConfig,\
                     _reportConfigReg, registerReportConfig                   
from Products.CMFPlone.utils import log
from Products.CMFPlone.utils import log_exc
from zope.event import notify
from zope.component import adapter
from events import IObjectAddedEvent, IObjectDeletedEvent, IObjectChangedEvent, ObjectAddedEvent, ObjectDeletedEvent, ObjectChangedEvent
import transaction
from pprint import pprint
import copy
import csv
from Products.Archetypes.utils import contentDispositionHeader
import cStringIO
import os
import tempfile, zipfile
from Products.Archetypes.utils import contentDispositionHeader
from zope.contenttype import guess_content_type
from DateTime import DateTime
from Products.CMFPlone.utils import safe_unicode
from datetime import datetime
from docpool.dbaccess.content.registry import *
from docpool.dbaccess.security import DefaultSecurity
from docpool.dbaccess.interfaces import IDataSecurity, IProtectedEntityClass
from zope.component import getMultiAdapter
from docpool.dbaccess.utils import stringFromDatetime, dtFromString

from zope.pagetemplate.pagetemplate import PageTemplate
from docpool.dbaccess.content.errors import ObjectDuplicateException
from docpool.dbaccess.interfaces import IAuditing
from zope.component.hooks import getSite
##/code-section imports 

from docpool.dbaccess.config import PROJECTNAME

from docpool.dbaccess import DocpoolMessageFactory as _


##code-section schema
##/code-section schema


##code-section afterfinalize
std_encoding = 'latin-1'
##/code-section afterfinalize


class dbadmin(object):
    implements(Idbadmin)
    """
    """

##code-section methods
    __allow_access_to_unprotected_subobjects__ = 1        
    def getRegisteredTypes(self, context):
        """
        Liefert die ids aller registrierten Typen.
        """
        ks = _ecreg.keys()
        liste = []
        # Hier pruefen wir aber noch Berechtigungen
        for k in ks:
            # print "checke", k
            klass = self.getKlass(k)
            security = self._getSecurity(klass, context)
            #print security
            if security.can_access():
                liste.append((k, _ecreg[k]['label'] ))
        liste.sort()
        #print 'registeredTypes'
        #print liste
        return liste
            
    def _getSecurity(self, klass, context):
        """
        """
        #print klass
        REQUEST = self._getRequest()
        user = REQUEST['AUTHENTICATED_USER']        
        try:
            if IProtectedEntityClass.providedBy(klass):
                a = getMultiAdapter((klass, user,), IDataSecurity)
            else:
                a = DefaultSecurity(klass, user)
            a.setContextObj(context)
            return a
        except Exception, e: # Wenn keiner definiert ist bzw. die Interfaces fehlen, dann greift der Default
            log_exc(e)
            a = DefaultSecurity(klass, user)
            a.setContextObj(context)
            return a
                    
    def edit_def(self, typ, from_ec=False, makeFS=True, readonly=False, security=None):
        """
        Liefert das Fieldset zum Editieren von Objekten vom Typ 'typ'.
        Wenn 'from_ec' == True, wird in jedem Fall die Definition aus
        dem EntityConfig Objekt geholt. 
        Ansonsten wird auch die Registry befragt, die aber nicht 
        unbeding auch einen Eintrag haben muss.
        @param makeFS: obsolet
        @param readonly: Liefert eine schreibgeschützte Variante des Formulars
        @return: ein dictionary {'form': FieldSet, 'prolog': HTML, 'epilog': HTML, 'allowMinor': boolean, ...}  
        """
        fields = None
        klass = None
        typ = typ.lower()
        if not from_ec:
            if _ecreg.has_key(typ): 
                fields = _ecreg[typ]['edit_def']
                klass = _ecreg[typ]['klass']
                            
        if callable(fields): # Funktion statt fertiges Formular
            fields = fields(security)
            
        if type(fields) != type({}): # Ist noch kein dictionary
            fields = {'form': fields, 'prolog': None, 'epilog': None, 'allowMinor': False}
             
        if readonly: # on the fly...
            form = copy.copy(fields['form'])
            form.readonly = True
            fields['form'] = form
        return fields

    def create_def(self, typ, from_ec=False, makeFS=True, readonly=False, security=None):
        """
        Liefert das Fieldset zum Anlegen von Objekten vom Typ 'typ'.
        Wenn 'from_ec' == True, wird in jedem Fall die Definition aus
        dem EntityConfig Objekt geholt. 
        Ansonsten wird auch die Registry befragt, die aber nicht 
        unbeding auch einen Eintrag haben muss.
        @param makeFS: obsolet
        @param readonly: wird hier ignoriert
        @return: ein dictionary {'form': FieldSet, 'prolog': HTML, 'epilog': HTML, 'allowMinor': boolean, ...}  
        """
        fields = None
        klass = None
        
        typ = typ.lower()
        if not from_ec:
            if _ecreg.has_key(typ):
                fields = _ecreg[typ].get('create_def', None)
                klass = _ecreg[typ]['klass']

        if callable(fields): # Funktion statt fertiges Formular
            fields = fields(security) # immer Kontext mitliefern
            
        if type(fields) == type({}): # Ist schon ein dictionary
            return fields
        else: # Dummy-Werte einfügen
            return {'form': fields, 'prolog': None, 'epilog': None, 'allowMinor': False} 


    def list_def(self, typ, from_ec=False, makeGrid=True, security=None):
        """
        Liefert das Grid fuer die tabellerarische Anzeige von Objekten vom Typ 'typ'.
        Wenn 'from_ec' == True, wird in jedem Fall die Definition aus
        dem EntityConfig Objekt geholt. 
        Ansonsten wird auch die Registry befragt, die aber nicht 
        unbeding auch einen Eintrag haben muss.
        Wenn 'makeGrid' == True, dann liefert die Methode ein fertiges Grid.
        Ansonsten nur die Feldnamen.
        """
        fields = None
        klass = None

        typ = typ.lower()
        if not from_ec:
            if _ecreg.has_key(typ):
                fields = _ecreg[typ]['list_def']
                klass = _ecreg[typ]['klass']

        if callable(fields): # Funktion statt fertiges Formular
            fields = fields(security) # immer Kontext mitliefern
            
        if type(fields) == type({}): # Ist schon ein dictionary
            return fields
        else: # Dummy-Werte einfügen
            return {'form': fields, 'prolog': None, 'epilog': None} 

    def filter_def(self, typ, from_ec=False, makeFS=True, security=None):
        """
        Liefert das Fieldset zum Filtern von Objekten vom Typ 'typ'.
        Wenn 'from_ec' == True, wird in jedem Fall die Definition aus
        dem EntityConfig Objekt geholt. 
        Ansonsten wird auch die Registry befragt, die aber nicht 
        unbeding auch einen Eintrag haben muss.
        Wenn 'makeFS' == True, dann liefert die Methode ein fertiges Fieldset.
        Ansonsten nur die Feldnamen.
        """
        fields = None
        klass = None

        typ = typ.lower()
        if not from_ec:
            if _ecreg.has_key(typ):
                fields = _ecreg[typ]['filter_def']
                klass = _ecreg[typ]['klass']

        if callable(fields): # Funktion statt fertiges Formular
            fields = fields(security)

        if type(fields) == type({}): # Ist schon ein dictionary
            return fields
        else: # Dummy-Werte einfügen
            return {'form': fields } 
    
    def sort_default(self, typ, from_ec=False):
        """
        Liefert das Feld, nachdem sortiert werden soll, wenn nichts anderes angegeben ist.
        Wenn 'from_ec' == True, wird in jedem Fall die Definition aus
        dem EntityConfig Objekt geholt. 
        Ansonsten wird auch die Registry befragt, die aber nicht 
        unbeding auch einen Eintrag haben muss.
        """
        typ = typ.lower()
        if not from_ec:
            if _ecreg.has_key(typ):
                return _ecreg[typ]['sort_default']

        return None
    
    def pkfields(self, typ):
        """
        Liefert die Namen der Felder, welche den PK definieren.
        """
        typ = typ.lower()
        if _ecreg.has_key(typ):
            klass = _ecreg[typ]['klass']                       # Python Klasse bestimmen
            cm = class_mapper(klass)                                # SA Mapper dieser Klasse holen

            if cm:
                return [c.key for c in cm.primary_key]
            else:
                return []
        else:
            return []
            
    def getKlass(self, typ):
        """
        Liefert die Python Klasse zu 'typ'
        """
        typ = typ.lower()
        if _ecreg.has_key(typ):
            klass = _ecreg[typ]['klass']                       # Python Klasse bestimmen
            return klass
        else:
            return None
        
    def getLabel(self, typ):
        """
        Liefert den Klartextnamen fuer den typ.
        """
        typ = typ.lower()
        if _ecreg.has_key(typ):
            label = _ecreg[typ]['label']
            return label
        else:
            return typ.capitalize()
        
            
    def getClassByName(self, klassmodule, klassname):
        """
        Liefert das Klassenobjekt zur Klasse 'klassname', definiert im Modul 'klassmodule'.
        """
        klass = getattr(sys.modules[klassmodule], klassname)
        return klass

    def getListViewObj(self, request, context):
        """
        """
        return forms.ListView(self, request, context)
    
    def getSEListViewObj(self, request, context, typ, filter, parentView):
        """
        """
        return forms.SEListView(self, request, context, typ, filter, parentView)

    def getEditViewObj(self, request, create, context):
        """
        """
        return forms.EditView(self, request, create, context)
            

    def getStructuredEditViewObj(self, request, create, context):
        """
        """
        return forms.StructuredEditView(self, request, create, context)
    

    def objekteSuchen(self, typ, filter=None, sort_on='', sort_order='ascending', limit=0):
        """
        filter ist eine Liste von Tupeln (attname, wert)
        sort_on ist der Name eines Attributs oder eine Liste von Namen
        """
        #print typ, filter
        klass = self.getKlass(typ)
        if sort_order == 'ascending':
            sfun = asc
        else:
            sfun = desc
        sort_join_field = None
        if type(sort_on) == list:
            sort = tuple([ sfun(getattr(klass,att)) for att in sort_on ])
        else: 
            if sort_on:
                if sort_on.find('|') != -1:
                    parts = sort_on.split('|')
                    sort_join_field, styp, sort_attr = parts[0], parts[1], parts[2]
                    sklass = self.getKlass(styp)
                    sort = (sfun(getattr(sklass,sort_attr)), )
                else: 
                    sort = (sfun(getattr(klass,sort_on)), )
        q = __session__.query(klass)
        if sort_join_field:
            q = q.join(sort_join_field)
        if sort:
            q = q.order_by(*sort)
        if filter:
            krit = []
            for f in filter:
                # Zuerst spezielle Faelle behandeln
                if type(f[1]) == list:
                    # wenn der wert eine Liste ist, so gucken wir per SQL-IN nach den elementen der sequenz
                    krit.append(getattr(klass, f[0]).in_(f[1]))
                elif f[0].find('__') != -1: # Spezieller Filter mit mehreren Feldern
                    names = f[0].split('__')
                    val = f[1]
                    att = getattr(klass, names[0])
                    t = getattr(att.parententity.c, att.key).type.__class__.__name__
                    if len(val) > 4:
                        if val[0] == '%':
                            val = val[1:]
                        if val[-1] == '%':
                            val = val[:-1]
                    else:
                        val = None
                    if val and t == "DateTime":
                        val = dtFromString(val)
                    if names[1] == 'von' and val:
                        krit.append(att >= val)
                        #print "von", val
                    elif names[1] == 'bis' and val:
                        krit.append(att <= val)
                        #print "bis", val
                else: # Jetzt die normalen Typen
                    a = getattr(klass, f[0])
                    # Jetzt den Namen des Typs auf verschlungenen Wegen beschaffen
                    t = getattr(a.parententity.c, a.key).type.__class__.__name__
                    if t == 'Boolean':
                        v = f[1]
                        if v:
                            if v == 'True':
                                v = True
                            elif v == 'False':
                                v = False
                            else:
                                try: # Es sollte eine Zahl sein
                                    v = int(v)
                                    if v:
                                        v = True
                                    else:
                                        v = False 
                                except:
                                    v = True
                        else:
                            v = False
                        krit.append(a == v)
                    elif t == 'Integer':
                        v = f[1]
                        if type(v) != int:
                            if v:
                                v = int(v[1:-1]) # % entfernen
                        krit.append(a == v)
                    elif type(f[1]) == str or type(f[1]) == unicode:
                        if f[1] == 'is Null':
                            krit.append(a == None)
                        elif f[1] == 'is not Null':
                            krit.append(a != None)
                        # ansonsten handelt es sich um ein LIKE
                        else:
                            krit.append(a.like(f[1].replace('*','%')))
                    else:
                        krit.append(a == f[1])
                    # TODO: was machen wir bei boolschen Werten?
            if len(krit) > 1:
                krit = tuple(krit)
                filter = and_(*krit)
            else:
                filter = krit[0]
#            print filter
            q = q.filter(filter)
        
        if limit:
            q = q.limit(limit)
        
        #print q.statement
        return q.all()
        
    def _extractData(self, request, typ):
        """
        Holt alle Felder aus dem Request, die sich auf Eingaben zu 'typ' beziehen.
        (Formalchemy generiert Namen fuer Felder, die mit dem Namen des Typs beginnen.)
        """
        typ = typ.split('_')[0] # Zusammengesetzte Typnamen beachten
        data = {}
        for key in request.keys():
            if key.lower().startswith(typ.lower()):
                data[key] = request[key]
                if type(data[key]) == type(''):
                    data[key] = data[key].decode('utf-8')
        #print data
        return data  
           
    def getPKDict(self, typ, pkvals):
        """
        """
        pkfields = self.pkfields(typ)
        print pkfields, pkvals
        assert(len(pkfields) == len(pkvals))
        i = 0
        res = {}
        for pkfield in pkfields:
            res[pkfield] = pkvals[i]
            i += 1
        #print res
        return res
            
    def objektdatensatz(self, typ, **pkvals):
        """
        """
        klass = self.getKlass(typ)
        try:
            res = __session__.query(klass).filter_by(**pkvals).one()
            return res
        except Exception, e:
            log_exc(e)
            return None 
    
    def ersterobjektdatensatz(self, typ, **filtervals):
        """
        """
        klass = self.getKlass(typ)
        try:
            res = __session__.query(klass).filter_by(**filtervals).all()
            if len(res) > 0:
                return res[0]
        except:
            return None 

    def _diff(self, obj, data):
        """
        Bestimmt die Aenderungen bei einem Objekt in Form eines Dictionarys zur Weiterverarbeitung.
        { fname : (old_value, new_value), ... }
        """
        res = {}
        for f in data.keys():
            fname = f.split('-')[-1] # Name des Feldes
            
            new_value = data[f]
            old_value = getattr(obj, fname)
            if isinstance(old_value, int):
                try:
                    new_value = int(new_value)
                except Exception, e:
                    log_exc(e)
                    log_exc(fname)
            
            if new_value != old_value:
                if new_value or old_value: # Nicht bei Variationen von 'nichts'
                    res[fname] = (old_value, new_value)
                    #print "%s: %s -> %s" % (fname, old_value, new_value)
        log(res)
        return res        
        
    def objektSpeichern(self, request, context=None):
        """
        """
        log("objektSpeichern")
        typ = request.get('typ')
        klass = self.getKlass(typ)
        isMinor = int(request.get('minor', 0))
        security = self._getSecurity(klass, context)
        data = self._extractData(request, typ)
        print data
        obj = None
        kwargs = {}
        defs = None

        d = None
        
        if not request.get('create', False):
            log("objektAendern")
            pk = eval(request.get('pk', "()"))
            pkvals = self.getPKDict(typ, pk)
            # print pkvals
            obj = self.objektdatensatz(typ, **pkvals)
            # print obj
            d = self._diff(obj, data)
            if not d: # Keine Aenderungen!
                # print "no diff"
                return
            if IAuditing.providedBy(obj):
                obj.wasUpdated(self)
            defs = self.edit_def
        else:
            log("objektAnlegen")
            obj = klass
            kwargs['session'] = __session__
            defs = self.create_def                        
        try:
            #print data
            fsobj = defs(typ, security=security)['form'].bind(obj, data = data,**kwargs)
        except Exception, e:
            log_exc(e)
            fsobj = defs(typ, security=security)['form'].bind(obj(), data = data,**kwargs)
        valid = fsobj.validate()
        moeglicheFehler = fsobj.render()
        # print moeglicheFehler
        result = None
        if valid:
            #print "valid", valid
            fsobj.sync()
            notUnique = hasattr(fsobj.model, 'checkUnique') and fsobj.model.checkUnique() or None
            log(notUnique)
            if notUnique:
                log('Dieser Datensatz ist bereits vorhanden!! dbadmin')
                transaction.abort()
                raise ObjectDuplicateException(notUnique, moeglicheFehler)
            __session__.flush()
            result = hasattr(fsobj.model, 'getPrimaryKeyValue') and fsobj.model.getPrimaryKeyValue() or None
            #print "flush"
            if not request.get('create', False): # UPDATE
                if not isMinor:
                    #print obj.to_dict()
                    #print d
                    notify(ObjectChangedEvent(obj, self, d, context))
            else:
                if IAuditing.implementedBy(klass):
                    # print "wasCreated"
                    fsobj.model.wasCreated(self)
                    __session__.flush()
                if not isMinor:
                    notify(ObjectAddedEvent(fsobj.model, self, data, context))
        else:
            result = moeglicheFehler
#            .replace('Please enter a value', 'Eingabe erforderlich!')\
#                                   .replace('Value is not an integer', 'Zahl eingeben!')
        #print result
        return result

    def objekteSpeichern(self, request, context=None):
        """
        Speichert alle Aenderungen, die ueber eine Tabelle (Grid) vorgenommen wurden.
        Jeder Datensatz wird einzeln gespeichert, um Events verarbeiten zu koennen. 
        """
        typ = request.get('typ')
        data = self._extractData(request, typ) # data enthaelt alle Felder der Tabelle
        # Jetzt muessen alle Zeilen identifiziert und einzeln behandelt werden.
        # print "objekteSpeichern"
        # print data
        datadict = _prepareGridData(data)
        
        for pk in datadict.keys():
            if pk and pk != '_':
                self.objektSpeichern(datadict[pk])
                transaction.commit() # Solange es keinen Fehler gibt, committen.

    def objekteLoeschen(self, request, context=None):
        """
        """
        typ = request.get('typ')
        klass = self.getKlass(typ)
        zuloeschen = request.get('objsel',[])
        if zuloeschen:
            for zl in zuloeschen:
                pkvals = self.getPKDict(typ, eval(zl))
                obj = self.objektdatensatz(typ, **pkvals)
                notify(ObjectDeletedEvent(obj, self, context)) # bevor es aus der DB verschwindet...
                __session__.delete(obj)
                __session__.flush()
        else:
            return
    
    def isManager(self):
        """
        """
        pass
    
    def cleanForm(self, typ, form):
        """
        Alle Parameter aus dem Form entfernen, die nicht gebraucht werden, damit der Request URL nicht zu lang wird
        """
        typ = typ.capitalize()
        for key in form.keys():
            if not (key.startswith(typ) or key in ['typ', 'sort_on', 'sort_order']):
                del form[key]

    def objekteImportieren(self, typ, importfile, request, context=None):
        """
        """
        try:
            meldung, status = imports.genericImportFromCSV(self, importfile, typ, request, context=context)
            log("Daten importiert.")
            return meldung, status
        except "Exception", e:
            log_exc("Daten konnten nicht importiert werden: %s" % importfile)
            return [ str(e) ], False
    
    #ALLES FUER EXPORT    
    def getRequestFilter(self, typ, request):
        """
        """
        of = self._extractData(request, typ)
        res = []
        for k in of.keys():
            if of[k]:
                fname = k.split('-')[-1]
                if type(of[k]) == type([]):
                    res.append((fname, of[k]))
                elif len(of[k]) > 0:
                    res.append((fname,'%' + of[k].replace('*','%')+'%'))
        return res
    
    def latin_1_encode(self, dict, encoding):
        """
        Sonderbehandlung fuer Datumswerte und Boolean. Unicode Handling
        """
        for field, value in dict.iteritems():
            if type(value) == datetime:
                dict[field] = value.strftime('%d.%m.%Y %H:%M:%S')
            elif type(value) == unicode:
                if value:
                    dict[field] = value.encode(encoding)
        return dict
    
    def getExportNames(self, typ):
        """
        """
        typ = typ.lower()
        if _exportConfigReg.has_key(typ):
            configs = _exportConfigReg[typ]
            return [ c[0] for c in configs ]
        else:
            return [ 'Standard' ]
    
    
    def exportObjektListe(self, typ, objektlisteTyp, delimiter=';', exportname='Standard'):
        """
        """
        return self.exportObjekte(typ, None, None, None, delimiter, exportname, objektlisteTyp)
    
    def exportObjekte(self, typ, sort_on, sort_order, filter={}, delimiter=';', exportname='Standard', objektlisteTyp=None, justData=False, encoding=None):
        """
        Exportiert Entities aus den Tabellenansichten.
        """
        csvdata = None
        REQUEST = self._getRequest()
        # Erstmal nur Entities
        if self.isExportable(typ):
            klasse = self.getKlass(typ)
            
            #Spaltennamen der Entity
            column_names_meta = [p.key for p in klasse.mapper.iterate_properties \
                                 if isinstance(p, ColumnProperty)]
            
            column_names = column_names_meta
            exportConfigs = _exportConfigReg.get(typ, [])
            exportConfig = None
            for ec in exportConfigs:
                if ec[0] == exportname:
                    exportConfig = ec[1]
            column_def = column_names_meta
            spalten = []
            #Wenn es eine Exportkonfiguration fuer die Entity gibt, dann verwende deren Optionen.
            if exportConfig:
                if not encoding:
                    e = exportConfig.get('encoding', None)
                    if e:
                        encoding = e
                felder = exportConfig['felder'][:]
                if exportConfig['zusatzFelder']:
                    felder.extend(exportConfig['zusatzFelder'])
                if felder:
                    column_def = felder[:]               
                    for column in column_def:
                        spalte = {'name':None, 'typ':None, 'fk_spalte':None, 'fk_typ':None}
                        if column.find('|') != -1: # FK Definition
                            parts = column.split('|')
                            spalte['fk_name'], spalte['fk_typ'], spalte['fk_spalte'] = parts[0], parts[1], parts[2]
                            spalte['name'] = column.lower()
                        elif column.find(':') != -1: # Typbezeichnung vorhanden <Name>:<int, date oder bool>
                            parts = column.split(':')
                            spalte['name'], spalte['typ'] = parts[0].lower(), parts[1]
                        elif column.find('#') != -1: #Dummy Spalte <Name>#<Wert>
                            parts = column.split('#')
                            spalte['name'], spalte['dummywert'] = "%s#" % parts[0].lower(), parts[1]
                            spalte['dummy'] = True
                        elif column.find('=') != -1: #Spalte mit Ausdruck
                            parts = column.split('=', 1)
                            spalte['name'], spalte['expression'] = "%s=" % parts[0].lower(), parts[1]
                            spalte['computed'] = True
                            #print spalte
                        else: # Alle anderen Faelle
                            spalte['name'] = column.lower()
                        spalten.append(spalte)
                    column_names = [s['name'] for s in spalten]
                    # print column_names
            if not encoding:
                encoding = std_encoding
            objekte = []
            if objektlisteTyp is not None:
                objekte = objektlisteTyp
            else:        
                #Falls exklusiv Datensaetze ausgewaehlt wurden
                objekte = []
                objsel = REQUEST.get('objsel', [])
                if objsel:
                    for pks in objsel:
                        pkvals = self.getPKDict(typ, eval(pks))
                        objekte.append(self.objektdatensatz(typ, **pkvals))
                #ansonsten
                else:
                    objekte = self.objekteSuchen(typ, filter, sort_on=sort_on, sort_order=sort_order)
            # print 'Anzahlobjekte %d' % len(objekte)
            #Schreiben in CSV-Datei                
            text = cStringIO.StringIO()
            dw = csv.DictWriter(text, column_names, dialect=csv.excel, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_ALL)
            errors = 0
            for objekt in objekte:
                try:
                    row = {} 
                    obj_dict = {}
                    if exportConfig and exportConfig.has_key('methodeFuerZusatzFelder') and exportConfig['methodeFuerZusatzFelder']:
                        obj_dict = exportConfig['methodeFuerZusatzFelder'](self, objekt, exportConfig['zusatzFelder'])
                    else:
                        obj_dict = objekt.to_dict()
                    
                    
                    #log(obj_dict)
                    # dict speichern
                    # ueber spalten iterieren
                    # Art bestimmen: normal oder fk
                    # normal: s['name'] aus dict nehmen
                    # Dann noch Typkorrektur wenn noetig
                    # fk: fkobj = getattr(objekt, s['name']), fkval = getattr(fkobj, s['fk_spalte']
                    # Und dabei immer das dict fuer die jeweilige Zeile fuellen
                    if spalten:
                        for s in spalten:
                            dummy = s.get('dummy', False)
                            computed = s.get('computed', False)
                            fk_typ = s.get('fk_typ', None)
                            fk_spalte = s.get('fk_spalte', None)
                            styp = s.get('typ', None)
                            value = ''
                            if fk_typ:
                                fkobj = getattr(objekt, s['fk_name'])
                                if fkobj:
                                    value = getattr(fkobj, s['fk_spalte'])
                            elif dummy:
                                value = s.get('dummywert', '')
                            elif computed:
                                e = s.get('expression', '')
                                value = eval(e)
                            else:
                                value = obj_dict.get(s['name'], '')
                            #log("Wert: %s, Typ: %s" % (value, type(value)))
                            #print styp
                            #Umwandlung Typ Boolean nach Integer
                            if styp == 'float':
                                if value is not None:
                                    value = str(value).replace(".",",")
                            elif styp == 'int':
                                if value is not None:
                                    #print "konvertiere", value
                                    value = int(value)
                            elif styp == 'bool':
                                if value is not None:
                                    #print "konvertiere", value
                                    value = int(value)
                                else:
                                    value = 0
                            elif styp in ['date','datetime']:
                                if value:
                                    #print value, type(value)
                                    long = False
                                    if styp == 'datetime':
                                        long = True
                                    value = stringFromDatetime(value, long=long)
                                    #print value
                            elif styp in ['string']:
                                if value:
                                    value = str(value)
                            row[s['name']] = value
                    else:
                        row = obj_dict
                    dw.writerow(self.latin_1_encode(row, encoding))
                except Exception, e:
                    errors += 1
                    log_exc(e)
                    log(row)
            
            table_columns = delimiter.join(column_def) + '\n' + text.getvalue()
            tmpfilename = tempfile.mktemp()
            tmpfile = open(tmpfilename, "wb")
            tmpfile.writelines(table_columns)
            tmpfile.close()
            
            file = open(tmpfilename, "rb")
            csvdata = file.read()
            groesse = len(csvdata)
            file.close()
        
            try:
                os.remove(tmpfilename)
            except Exception, e:
                log_exc(e)
        
            if REQUEST is not None and not justData:
                RESPONSE = REQUEST.RESPONSE
                header_value = contentDispositionHeader('attachment', filename='%s_%s.csv' % (typ, DateTime().millis()), charset='latin-1')
                RESPONSE.setHeader("Content-disposition", header_value)
            
                RESPONSE.setHeader("Content-Type", 'text/csv')
                if groesse:
                    RESPONSE.setHeader("Content-Length", groesse)
            log('EXPORTFILTER: %s' % filter)
            log('EXPORTSORT_ON: %s' % sort_on)
            log('EXPORTSORT_ORDER: %s' % sort_order)
            log('%s von %s Objekten des Typs %s exportiert' % (len(objekte) - errors, len(objekte), typ))
        else:
            log('Dieser Typ: %s ist nicht exportfaehig, da keine to_dict-Methode implementiert ist.' % typ)
        return csvdata
    
    def reportObjekte(self, reportcontext, typ, sort_on, sort_order, filter={}, reportname='Standard', test=False, **templatevars):
        """
        @param reportcontext: context mit dem der Report erzeugt werden soll.
        @param typ: Entityname fuer die Datenbankabfrage zur Bestimmung des Reportumfangs.
        @param sort_on: DB-Sortierattribut
        @param sort_order: DB-Sortierreihenfolge
        @param filter: Moegliche Filterwerte fuer die Abfrage.
        @param reportname: Name des registrierten Reports
        @param test: Attribut zu Testzwecken mit einem echten View-Template
        """
        log('reportObjekte')
        reportReg = _reportConfigReg.get(typ, [])
        reportConfig = None
        #print 'filter ', filter
        REQUEST = self._getRequest()
        
#        print reportReg
#        print reportname
        
        for ec in reportReg:
            if ec[0] == reportname:
                reportConfig = ec[1]
#        print reportConfig
        if reportConfig:
#            print 'reportConfig gefunden'
            reportTemplateName = reportConfig.get('reportTemplateName')
            if reportTemplateName:
#                print 'TemplateName gefunden'
                objekte = []
                objsel = REQUEST.get('objsel', [])
                if objsel:
                    for pks in objsel:
                        pkvals = self.getPKDict(typ, eval(pks))
                        
                        objekte.append(self.objektdatensatz(typ, **pkvals))
                #ansonsten
                else:
                    objekte = self.objekteSuchen(typ, filter, sort_on=sort_on, sort_order=sort_order)
                
                # print len(objekte)
                
                if not templatevars:
                    templatevars = {'objekte':objekte,
                                    'reportcontext':reportcontext}
                else:
                    templatevars['objekte'] = objekte
                    templatevars['reportcontext'] = reportcontext
                
                template_obj = None

                if reportcontext.getField(reportTemplateName):
                    template_obj = PageTemplate()
                    content = reportcontext.getField(reportTemplateName).getRaw(reportcontext)#.read()
#                    print content
                    template_obj.pt_edit(content,'text/html')
                else:
                    if test:
                        return templatevars['objekte']
                    template_obj = getattr(reportcontext, reportTemplateName)
                
#                print template_obj
#                return template_obj(**templatevars)    
                return safe_unicode(template_obj(**templatevars)) 
                        
    def isReportable(self, typ):
        """
        """
        typ = typ.lower()
        isReportable = []
        reportReg = _reportConfigReg.get(typ, [])
        for report in reportReg:
            isReportable.append(report[0])
        return isReportable    
    
    def isExportable(self, typ):
        """
        """
        isExportable = False
        if typ:
            klasse = self.getKlass(typ)
            if hasattr(klasse, 'to_dict'):
                isExportable = True
        return isExportable
    
    def getRollen(self, nutzerobjekt, moeglicheRollen=[]):
        """
        """
        nutzerrollen = {}
        if moeglicheRollen:
            for rolle in moeglicheRollen:
                nutzerrollen[rolle] = nutzerobjekt.has_role(rolle)
        return nutzerrollen
    
    def prepareEditURL(self, typ, obj):
        """
        """
        return (str(obj), 'objekt_edit?typ=%s&pk=%s&herkunft=objekt_liste?typ=%s' % (typ, str(obj._sa_instance_state.key[1]), typ))
            
    def _getRequest(self):
        """
        """
        plone = getSite()
        return plone.REQUEST      
##/code-section methods 

##code-section bottom
def _prepareGridData(data):
    """
    Ordnet alle Formularfelder in data entsprechend ihrer zugehoerigen Objekte.
    Liefert ein Dictionary der Form { pk_string : { fn1 : fval1, fn2 : fval2 , ...} }
    """
    res = {}
    for fn in data.keys():
        # print fn
        pkexpr = fn.split('-')[1] # Primary key steht in der Mitte
        if len(pkexpr) < 1: # Kein Editformularfeld, sondern vom Filterformular!
            continue
        typ = fn.split('-')[0].lower() # Typ am Anfang
        if not res.has_key(pkexpr): # weiteres Objekt
            res[pkexpr] = { fn : data[fn], 'typ' : typ, 'pk' : str(pkexpr.split('_')) }
        else: # weiterer Wert fuer bereits erkanntes Objekt
            res[pkexpr][fn] = data[fn]
    # print "prepareGridData"
    # print res
    return res

##/code-section bottom 

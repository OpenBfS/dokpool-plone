# -*- coding: utf-8 -*-

from elan.dbaccess.utils import unicode_csv_reader, dtFromString
from Products.CMFPlone.utils import log, log_exc, safe_unicode
##code-section imports
from elan.dbaccess.dbinit import __metadata__, __session__
from zope.event import notify
from elan.dbaccess.content.events import ObjectChangedEvent,\
    ObjectAddedEvent

metadata = __metadata__
session = __session__

from elixir import *

import transaction
from StringIO import StringIO
from datetime import datetime # mindestens für Expressions hilfreich

def genericImportFromCSV(tool, file, typ, request, delimiter=';', updatespalten=[], context=None):
    """
    @param updatespalten: Listet die Spalten, die beim Update berücksichtigt werden sollen. Das erlaubt ein Subset,
    während beim INSERT immer alle gültigen Spalten genutzt werden.
    """
    from elan.dbaccess.content.dbadmin import getAllEntityFields # zyklischen Import vermeiden
    klass = tool.getKlass(typ)
    pkfields = tool.pkfields(typ)
    pkfields = set(pkfields) # Hier kann ein Feld doppelt genannt werden
    efields = getAllEntityFields(klass)
    #print pkfields
    #print efields
    if type(file) in (type(""), type(u"")):
        file = StringIO(file)
        meldung = [ "Import aus Zeichenkette fuer %s" % (typ) , "",  "" ]
    else:
        meldung = [ "Import von Datei %s fuer %s" % (file.filename, typ) , "",  "" ]
    kopfzeile = file.readline()
    kopfzeile = kopfzeile.strip() # Zeilenende weg


    status = True # = OK
    
    spalten = kopfzeile.split(delimiter)
    # So, jetzt haben wir die Namen der zu importierenden Felder.
    # Wir muessen feststellen,
    # a) ob die Primaerschluesselspalten dabei sind und
    # b) welche Felder ggf. nicht ueberschrieben werden sollen und
    # c) welche Fremdschluessel behandelt werden muessen.
    #print spalten
        
    alle = []
    ungueltig = []
    fk = {}
    numerisch = []
    gleitkomma = []
    bool = []
    daten = []
    computed = {}
    unique = []
    
    for spalte in spalten:
        isComputed = False
        expression = None
        isUnique = False
        if spalte.startswith("*"): # Unique
            isUnique = True
            spalte = spalte[1:]
        if spalte.find('=') != -1: # Angabe eines Ausdrucks zur Berechnung
            parts = spalte.split('=')
            spalte, expression = parts[0], parts[1]
            isComputed = True
        if spalte.find('|') != -1: # FK Definition
            parts = spalte.split('|')
            spalte, fktyp, fkspalte = parts[0], parts[1], parts[2]
            fkklass = tool.getKlass(fktyp)
            fkcol = getattr(fkklass,fkspalte)
            fk[spalte.split(':')[0]] = (fkklass, fkcol)
        if spalte.find(':') != -1: # Typbezeichnung vorhanden
            parts = spalte.split(':')
            spalte, styp = parts[0], parts[1]
            if styp in ['date', 'datetime']:
                daten.append(spalte)
            elif styp == 'float':
                gleitkomma.append(spalte)
            elif styp == 'int':
                numerisch.append(spalte)
            elif styp == 'bool':
                bool.append(spalte)
        if isComputed:
            computed[spalte] = expression
                
        if not spalte in efields and not spalte in pkfields: # Wenn die Spalte unzulässig ist
            ungueltig.append(spalte)
            if spalte in numerisch:
                numerisch.remove(spalte)
            if spalte in gleitkomma:
                gleitkomma.remove(spalte)
            if spalte in daten:
                daten.remove(spalte)
            if spalte in bool:
                bool.remove(spalte)
            if computed.has_key(spalte):
                del computed[spalte]
        elif isUnique:
            unique.append(spalte)
        alle.append(spalte)
        
           
            
    mitpk = True
    for pkfield in pkfields:
        #print pkfield
        #print alle
        if pkfield not in alle:
            mitpk = False

    meldung.append(u"Spalten: " + ", ".join(alle))
    meldung.append(u"Enthalten Schlüssel? %s" % (mitpk and "Ja" or "Nein"))
    meldung.append(u"Eindeutige Werte beachten: %s" % ", ".join(unique))
    meldung.append(u"Ignorierte Spalten: %s" % ", ".join(ungueltig))
    meldung.append(u"")
    
    #print "mit PK?", mitpk

    #print alle
    #print ungueltig
    #print fk
    #print numerisch
    #print daten
    
    if len(alle) == 0:
        # Nichts zu importieren, ungueltige Daten
        meldung.append(u"Keine Spaltennamen gefunden.")
        status = False
        return status, meldung
    reader = unicode_csv_reader(file, delimiter=delimiter, fieldnames=alle)
    
    inserts = 0
    updates = 0
    summe = 0
    fehler = 0
    
    for row in reader:
        #log("%d" % summe)
        orig = row.copy()
        try:
            for u in ungueltig:
                del row[u]
            

            for c in computed.keys(): # Berechnete Werte eintragen
                e = computed[c] # Ausdruck
                v = eval(e) # Wert
                row[c] = v        
            
            fkerror = False
            for f in fk.keys(): # Jetzt die referenzierten Objekte bestimmen
                fkklass, fkcol = fk[f]
                if row[f]:
                    try:
                        if f in numerisch:
                            r = fkklass.query.filter(fkcol == int(row[f])).one() # FIXME: das funktioniert nur fuer Zeichenketten-Spalten
                        else:
                            r = fkklass.query.filter(fkcol == row[f]).one() # FIXME: das funktioniert nur fuer Zeichenketten-Spalten
                        row[f] = r
                    except Exception, e:
                        #print e
                        meldung.append(u"Kein Verweis '%s' gefunden - ignoriert" % row[f])
                        meldung.append(u"Daten: %s" % safe_unicode(str(orig)))
                        meldung.append(u"")
                        fkerror = True
                else:
                    row[f] = None
                    
            if fkerror:
                fehler += 1
                summe += 1
                continue
              
            # jetzt werden die Typen konvertiert soweit noetig, fehlende Werte werden geNULLt
            for d in daten:
                if row[d] and len(row[d]) > 2:
                    row[d] = dtFromString(row[d])
                else:
                    row[d] = None
            for n in numerisch:
                if row[n] or row[n] == 0:
                    row[n] = int(row[n])
                else:
                    row[n] = None
            for n in gleitkomma:
                if row[n] or row[n] == 0.0:
                    row[n] = float(row[n])
                else:
                    row[n] = None
            for n in bool:
                if row[n]:
                    v = row[n]
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
                    row[n] = v
                else:
                    row[n] = False
                    
            if not mitpk: # INSERT
                # print "INSERT"
                # TODO: hier ggf. unique Spalten checken
                if unique:
                    uk_ok = True
                    ukvals = {}
                    for f in unique:
                        if not row[f]: # Wert fehlt
                            uk_ok = False
                        else:
                            ukvals[f] = row[f]
                    if uk_ok: # Werte zum Check vorhanden
                        obj = tool.objektdatensatz(typ, **ukvals)
                        if obj: 
                            # Es gibt schon einen Eintrag.
                            # Also wird nicht importiert.
                            summe += 1
                            continue
                    
                neu = klass(**row)
                notify(ObjectAddedEvent(neu, tool, row, context))

                try:
                    transaction.commit()
                    inserts += 1
                except Exception, e:
                    #print e
                    transaction.abort()
                    meldung.append(u"Fehler: %s" % str(e))
                    meldung.append("Daten: %s" % safe_unicode(str(orig)))
                    meldung.append(u"")
                    fehler += 1
                    summe += 1
                    continue
            else: # potentiell UPDATE
                # Sind die PK Felder auch gefuellt fuer die Zeile?
                pk_ok = True
                pkvals = {}
                for f in pkfields:
                    if not row[f]: # Wert fehlt
                        pk_ok = False
                    else:
                        pkvals[f] = row[f]
                        del row[f]
                if pk_ok: # UPDATE
                    obj = tool.objektdatensatz(typ, **pkvals)
                    if obj: 
                        for cn in row.keys():
                            if not updatespalten or cn in updatespalten: # Ggf. nur ein Subset updaten
                                c = row[cn]
                                setattr(obj, cn, c)
                        notify(ObjectChangedEvent(obj, tool, {}, context))
                        transaction.commit()
                        updates += 1
                    else:
#                        fehler += 1
                        meldung.append(u"Kein Objekt zum Schlüssel %s gefunden - neu angelegt" % str(pkvals))
                        meldung.append(u"Daten: %s" % safe_unicode(str(orig)))
                        meldung.append(u"")
                        neu = klass(**row)
                        for f in pkfields:
                            c = pkvals[f]
                            setattr(neu, f, c)
                        transaction.commit()
                        inserts += 1
                else: # INSERT
                    neu = klass(**row)
                    notify(ObjectAddedEvent(neu, tool, row, context))
                    transaction.commit()
                    inserts += 1
        except Exception, e:
            transaction.abort()
            fehler += 1
            meldung.append(u"Fehler: %s" % str(e))
            meldung.append("Daten: %s" % safe_unicode(str(orig)))
            meldung.append(u"")
            log(str(orig))
            log_exc(e)
        summe += 1
    meldung.append(u"Insgesamt behandelt: %d" % summe)
    meldung.append(u"Davon neu: %d" % inserts)
    meldung.append(u"Davon geändert: %d" % updates)
    if fehler:
        status = False
        meldung.append(u"Fehlerhafte Datensätze: %d" % fehler)
    else:
        meldung.append(u"Keine Fehler")
    return meldung, status
# -*- coding: utf-8 -*-
__author__ = 'Condat AG'
__docformat__ = 'plaintext'

#from elixir import *
from elan.dbaccess.dbinit import __session__

from formalchemy import FieldSet, Grid
from formalchemy import config
from formalchemy import templates
from formalchemy import types
from formalchemy import fields
from formalchemy import Field
from formalchemy import FieldRenderer, CheckBoxFieldRenderer
from Products.Archetypes.debug import log_exc
from formalchemy.fields import RadioSet
from formalchemy import helpers as h
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log_exc
from plone.memoize.view import memoize
from Products.CMFPlone.PloneBatch import Batch
from ZTUtils import make_query
from zope.component import getMultiAdapter
from zope.interface import providedBy
from elan.dbaccess.security import DefaultSecurity
from elan.dbaccess.interfaces import IDataSecurity, IProtectedEntityClass, IAuditing
from elan.dbaccess.utils import stringFromDatetime
from Products.Archetypes.utils import shasattr
from elan.dbaccess import DocpoolMessageFactory as _

from AccessControl import Unauthorized

config.date_format = '%d.%m.%Y'
config.date_edit_format = 'd-m-y'

import os
tdir = os.path.join(os.path.dirname(__file__), '..', 'fa_tmpl')
# print tdir

config.engine = templates.TempitaEngine(
               directories=[tdir])


listbutton_defs = {
# TODO
               }
# Alternative: class_mapper(klass).primary_key, liefert Column-Objekte

class BatchBase(object):
    """Default view
    """
    
    ##code-section methods1
    __allow_access_to_unprotected_subobjects__ = 1
    
    def __init__(self, tool, request, context):
        self.context = context
        self.request = request
        self.tool = tool
        self.__name__= ''
        
#    @memoize
    def getBatchStart(self):
        return self.request.form.get('b_start', 0)

#    @memoize
    def getBatchSize(self): 
        return self.request.get('eineseite', None) and 100000 or 10;

#    @memoize
    def getBatchObj(self):
        # Batch(objekte, b_size, int(b_start), pagerange=10, orphan=2,quantumleap=1);
        b_start = self.getBatchStart()
        items = self._getItems()
        return Batch(items, self.getBatchSize(), b_start, pagerange=10, orphan=2, quantumleap=1)

#    @memoize
    def anzobj(self):
        return len(self._getItems())
    
#    @memoize
    def seitennr(self):
        return self.getBatchObj().pagenumber
    
#    @memoize
    def seitengesamt(self):
        return self.getBatchObj().numpages
        
#    @memoize
    def _getItems(self): 
        return []
    
#    @memoize
    def getItems(self):
        return self._getItems()
        
#    @memoize
    def getSorting(self):
        sort_on = self.request.form.get('sort_on', 'modified') # TODO: Veroeffentlichungsdatum
        sort_order = self.request.form.get('sort_order', 'reverse')
        return {'sort_on': sort_on, 'sort_order': sort_order}
    
    def sortURL(self, column):
        s = self.getSorting()
        so = 'ascending'
        if s['sort_on'] == column:
            so = 'reverse'            
            if s['sort_order'] == 'reverse':
                so = 'ascending'
        template_id = self.__name__
        if template_id == 'view':
            template_id = None
        qry = make_query(self.request.form, {'sort_on':column, 'sort_order':so})
        if template_id:
            return "%s/%s?%s" % (self.context.absolute_url(), template_id, qry)
        else:
            return "%s?%s" % (self.context.absolute_url(), qry)

#    @memoize        
    def getSortOrder(self):
        sort_on = self.getSorting()['sort_on']
        sort_order = self.getSorting()['sort_order']
        if sort_order in ("reverse", "descending"):
            sort_order = 'desc'
        elif sort_order in ("ascending"):
            sort_order = 'asc'
        
        x = "%(sort_on)s_%(sort_order)s" % locals()
        return x

    def sortURLSelect(self, sort_on, sort_order):

        #template_id = self.__name__        
        # explicit is better than implicit
        #if template_id == 'view':
        #    template_id = None
            
        qry = make_query(self.request.form, {'sort_on' : sort_on, 
                                             'sort_order' : sort_order})
        #if template_id:
        return "%s?%s" % (self.__name__, qry)
            
    def getGridHTML(self):
        """
        """
        return ""
    ##/code-section methods1     

class ListView(BatchBase):
    """
    """
    
    ##code-section methods1
    def __init__(self, tool, request, context):
        BatchBase.__init__(self, tool, request, context)
        self.typ = hasattr(self, "typ") and self.typ or request.get('typ')
        self.__name__= 'objekt_liste'
        klass = self.tool.getKlass(self.typ)
        self.label = self.tool.getLabel(self.typ)
        self.exports = self.tool.getExportNames(self.typ)
        #print "Exporte:", self.exports
        self.multiexport = len(self.exports) > 1
        self.security = self.tool._getSecurity(klass, context)
        self.security.setView(self)
        self.can_access = self.security.can_access()
        gdef = self.tool.list_def(self.typ, security=self.security)
        #print gdef
        self.grid = gdef['form']
        self.prolog = gdef.get('prolog', None)
        self.epilog = gdef.get('epilog', None)
        self.sortNames = gdef.get('sortNames', None)
        self.importRestricted = gdef.get('importRestricted', False)
        fdef = self.tool.filter_def(self.typ, security=self.security)
        self.fform = fdef['form']
        self.filter = hasattr(self, "filter") and self.filter or fdef.get('filter', None)
        self.has_create = self.tool.create_def(self.typ, security=self.security)['form'] is not None

    def checkAccess(self):
        """
        """
        if not self.can_access:
            raise Unauthorized, "Keine Berechtigung fuer diesen Typ"
        else:
            return True
#    @memoize
    def _getFilter(self):
        if self.filter: # Voreingestellter Filter, injizieren
            if callable(self.filter):
                of = self.filter(self.context)
            else:
                of = self.filter
            for k in of.keys():
                print k, of[k]
                if not self.request.get(k, None): # Wenn noch nicht gesetzt
                    self.request.set(k, of[k])
        of = self._getObjectFields()
        # print of
        res = []
        for k in of.keys():
            if of[k]:
                fname = k.split('-')[-1]
                if type(of[k]) == type([]):
                    res.append((fname, of[k]))
                elif type(of[k]) == int:
                    res.append((fname, of[k]))
                elif len(of[k]) > 0:
                    res.append((fname,'%' + of[k].replace('*','%')+'%'))
        return res
    
#    @memoize
    def _getObjectFields(self):
        return self.tool._extractData(self.request, self.typ)
    
#    @memoize
    def _getItems(self):
        # TODO: Berechtigungen
        # Begrenzen auf eine akzeptable Anzahl an Ergebnissen,
        # um die Massendaten bearbeitbar zu machen
        filter = self._getFilter()
        return self.tool.objekteSuchen(self.typ, filter, limit=10000, **self.getSorting()) 
            
#    @memoize
    def getBatchSize(self): 
        return self.request.get('eineseite', None) and 100000 or 25; # TODO: konfigurierbar im Tool

#    @memoize
    def getListButtons(self):
        #TODO: Berechtigungen
        b = []
        if self.security.can_delete_all():
            b.append(('delete',_(u'Delete'), 'return ' + _('sicherheitsabfrage')+'();'))
        if self.has_create and self.security.can_create():
            b.append(('create', _(u'New'), ''))
        return listbutton_defs.get(self.typ, b)
    
#    @memoize
    def isImportAllowed(self):
        """
        """
        user = self.context.REQUEST['AUTHENTICATED_USER']
        if self.importRestricted:
            return user.has_role("Manager")
        else:
            return self.security.can_update_all()

#    @memoize
    def getSorting(self):
        sort_on = self.request.form.get('sort_on') or self.tool.sort_default(self.typ) 
        sort_order = self.request.form.get('sort_order') or 'ascending'
        return {'sort_on': sort_on, 'sort_order': sort_order}
    
    def getGridHTML(self):
        """
        """
        return self.grid.bind(self.getBatchObj()).render()
    
    def getFilterHTML(self):
        """
        """
        fs = self.fform
        of = self._getObjectFields()
        #print of
        if of:
            fs = fs.bind(data=of)
        return fs.render()
        
    def getColumnNames(self):
        """
        """
        res = []
        collection = self.tool.list_def(self.typ)['form'].bind(self.getBatchObj())
        for field in collection.render_fields.itervalues():
            if field.key not in ['editlink','check']:
                res.append(field.key)
        return res
    
    def getSortNames(self):
        """
        """
        if self.sortNames is not None:
            return self.sortNames
        else:
            return self.getColumnNames()
    ##/code-section methods1     

class SEListView(ListView):
    
    def __init__(self, tool, request, context, typ, filter, parentView):
        self.typ = typ
        self.filter = filter
        self.parentView = parentView
        ListView.__init__(self, tool, request, context)
        self.__name__= 'objekt_seliste'

    def getListButtons(self):
        b = []
        if self.has_create and self.security.can_create():
            b.append(('create', _(u'New'), ''))
        return listbutton_defs.get(self.typ, b)

class EditView(object):

    def __init__(self, tool, request, create, context):
        # print "EditView"
        self.context = context
        self.request = request
        self.tool = tool
        self.typ = request.get('typ', None)
        self.create = create and True or False
        pk = request.get('pk', None)
        if not self.typ:
            if shasattr(context, "getStructuredType"):
                self.typ = context.getStructuredType()
        if not pk:
            if not self.create:
                if shasattr(context, "getPrimaryKey"):
                    pk = str(context.getPrimaryKey())
                else:
                    pk = '{}'
            else:
                pk = "[ '###' ]"
        self.pk = eval(pk) # 
        self.klass = self.tool.getKlass(self.typ)
        self.label = self.tool.getLabel(self.typ)
        self.security = self.tool._getSecurity(self.klass, context)
        self.security.setView(self)
        self.readonly = True
        self.can_delete = False    
        if self.create:
            if not self.security.can_create():
                raise Unauthorized, "Keine Berechtigung zum Erzeugen"
            else:
                defs = self.tool.create_def(self.typ, readonly=self.readonly, security=self.security)
                self.readonly = False
                self.sd = self.klass
                self.prolog = defs.get('prolog', None)
                self.epilog = defs.get('epilog', None)
                self.allowMinor = False
                self.form = defs['form']
                self.audit = None
         
        else:
            # print "edit"
            self.sd = self.tool.objektdatensatz(self.typ, **self.tool.getPKDict(self.typ, self.pk))
            # Hier muessen wir Edit-Rechte pruefen
            if (self.security.can_update_all() or self.security.can_update(self.sd)):
                self.readonly = False
            if (self.security.can_delete_all() or self.security.can_delete(self.sd)):
                self.can_delete = True
            # print self.readonly, self.can_delete
            defs = self.tool.edit_def(self.typ, readonly=self.readonly, security=self.security)
            self.prolog = defs.get('prolog', None)
            self.epilog = defs.get('epilog', None)
            self.form = defs['form']
            self.allowMinor = (not self.readonly) and defs.get('allowMinor', False)
            # print self.allowMinor
            if IAuditing.providedBy(self.sd): # Automatische Änderungprotokollierung aktiv
                self.audit = {'en': self.sd.erzeugungsnutzer or '---', 'ed' : self.sd.erzeugungsdatum and stringFromDatetime(self.sd.erzeugungsdatum, True) or '---', 'aen': self.sd.aenderungsnutzer or '---', 'aed': self.sd.aenderungsdatum and stringFromDatetime(self.sd.aenderungsdatum, True) or '---'}
            else:
                self.audit = None
            # print self.audit

        self.defaults = defs.get('defaults', None)
        self.can_access = self.security.can_access()
        if not self.can_access:
            raise Unauthorized, "Keine Berechtigung zum Zugriff auf diese Daten"
            
    @memoize
    def _getObjectFields(self):
        return self.tool._extractData(self.request, self.typ)
        
                
    def herkunft(self):
        """
        """
        h = self.request.get('herkunft', None) or self.request.get('HTTP_REFERER', None)
        if h and h.find('typ=') == -1:
            h = "%s?typ=%s" % (h, self.typ)
        return h
            
        
    def checkAccess(self):
        """
        """
        if not self.can_access:
            raise Unauthorized, "Keine Berechtigung fuer diesen Typ"
        else:
            return True
            
    def getPKValsAsString(self):
        """
        """
        return str(self.pk)


    @memoize
    def getEditButtons(self):
        b = []
        if not self.readonly:
            b.append(('save',_(u'Save'), ''))
        if self.can_delete:
            b.append(('delete',_(u'Delete'), 'return '+_('einfachesicherheitsabfrage')+'();'))
        return b

    def getFieldSetHTML(self):
        """
        Liefert HTML fuer das Edit Formular
        """
        formerror = self.request.get('formerror', None)        
        if formerror:
            return formerror
        else:
            pre = ""
            kwargs = {}
            defaults = {}
            form = self.form
            if self.defaults: 
                if callable(self.defaults):
                    of = self.defaults(self.context)
                else:
                    of = self.defaults
                if self.create: # Vgl. Filter Defaults
                    for k in of.keys():
                        pre = pre + "<input type='hidden' id='%s--%s' name='%s--%s:int' value='%s' />" % (self.sd.__name__, k, self.sd.__name__, k, of[k])
                else:
                    for key in of:
                        if hasattr(self.sd, key) and getattr(self.sd, key) is None:
                            setattr(self.sd, key, of[key])
            try:
                bf = form.bind(self.sd,**kwargs)
                html = bf.render()
            except Exception, e: # Hier gibt es leider einen Unterschied zwischen Elixir Entities und gemappten SA Klassen
                log_exc(e)
                html = form.bind(self.sd(),**kwargs).render()
            return pre + html
            
    def getCFieldSetHTML(self):
        """
        Liefert HTML fuer das Create Formular
        """
        kwargs = {}
        kwargs['session'] = __session__
        form = self.form
        # print "CFS"
        if self.defaults:
            # print "YES" 
            if callable(self.defaults):
                of = self.defaults(self.context)
            else:
                of = self.defaults
            #print "Defaults", of
            #print type(self.sd)
            for key in of:
                # print key
                if getattr(self.sd, key) is None:
                    # print of[key]
                    setattr(self.sd, key, of[key])
        try:
            return form.bind(self.sd,**kwargs).render()
        except Exception, e: # Hier gibt es leider einen Unterschied zwischen Elixir Entities und gemappten SA Klassen
            log_exc(e)
            return form.bind(self.sd(),**kwargs).render()
        
class StructuredEditView(EditView):
    
    def __init__(self, tool, request, create, context):
        EditView.__init__(self, tool, request, create, context)
        if not self.defaults:
            fkdefault = eval(self.request.get('fkdefault', '{}'))
            if fkdefault:
                self.defaults = fkdefault
        
    def subentities(self):
        """
        """
        return self.klass.subentities()
    
    def fkdefault(self):
        """
        """
        return { self.klass.fkName() : self.sd.id }

    def fkfilter(self, seklassname):
        """
        """
        return { seklassname + "--" + self.klass.fkName() : self.sd.id }
    
    def parentPath(self):
        pp = eval(self.request.get('bc', '[]'))
        return pp
    
    def breadcrumbs(self):
        """
        """
        bc = self.parentPath()
        #print bc
        if not bc or bc == 'None':
            bc = [(self.typ, self.pk)]
        else:
            bc.append((self.typ, self.pk))
        return bc
    
    def edit_url(self):
        """
        """
        pp = self.parentPath()
        ap = self.context.absolute_url() 
        if len(pp) > 0:
            h = "%s/struct_edit?typ=%s&pk=%s&bc=%s" % (ap, self.typ, self.pk, str(pp))
        else:
            h = "%s/struct_edit?typ=%s&pk=%s" % (ap, self.typ, self.pk)
        return h
        

    def herkunft(self):
        """
        """
        pp = self.parentPath()
        ap = self.context.absolute_url() 
        if len(pp) > 0:
            last = pp.pop()
            h = "%s/struct_edit?typ=%s&pk=%s&bc=%s" % (ap, last[0], last[1], str(pp))
        else:
            h = "%s/struct_edit?typ=%s&pk=%s" % (ap, self.typ, self.pk)
        return h
    
class NoneRenderer(FieldRenderer):
    def render(self, **kwargs):
        """render html for edit mode"""
        from formalchemy import helpers as h
        return h.text_field(self.name, value='', **kwargs)
     
    def render_readonly(self, **kwargs):
        """render html for read only mode"""
        return 'NULL'

class NoRenderer(FieldRenderer):
    def render(self, **kwargs):
        """render html for edit mode"""
        return ""
     
    def render_readonly(self, **kwargs):
        """render html for read only mode"""
        return ""


class JaNeinRenderer(CheckBoxFieldRenderer):
    def render_readonly(self, **kwargs):
        """render html for read only mode"""
        if self._value and self._value == 'True':
            return "Ja"
        else:
            return "Nein"
    


class DatePickerFieldRenderer(FieldRenderer):
    def render(self):
        value= self._value and self._value or ''
        vars = dict(name=self.name, value=value)
        return """
           <input id="%(name)s" name="%(name)s"
                  type="text" value="%(value)s">
           <script type="text/javascript">
             $('#%(name)s').datepicker({dateFormat: 'dd-mm-yy'})
           </script>
        """ % vars

class DateTimeAsTextRenderer(FieldRenderer):
            
    def _rbase(self):
        value= self._value and self._value or ''
        #print value
        if value:
            v1 = value.split(' ')
            
            v2 = v1[0].split('-')
            v2.reverse()
            
            v3 = v1[1][:5]
            
            value = "%s %s" % ( ".".join(v2), v3 ) 
        return value

    def _serialized_value(self):
        if self.params.has_key(self.name):
            v = self.params.getone(self.name)
            if v:
                v1 = v.split(' ') 
                if len(v1) == 2: # Wenn Zeit mit angegeben
                    v2 = v1[0].split('.')
                    v2.reverse()
                    v3 = v1[1]
                else: 
                    v2 = v1[0].split('.')
                    v2.reverse()
                    v3 = "00:00"
                value = "%s %s" % ('-'.join(v2), v3)
                return value
        else:
            return ''
        
    def render(self, **kwargs):
        value = self._rbase()
        return h.text_field(self.name, value=str(value), **kwargs)
    
    def render_readonly(self, **kwargs):
        """render html for read only mode"""
        return self._rbase()
    
class DateAsTextRenderer(FieldRenderer):
    
    def _serialized_value(self):
        if self.params.has_key(self.name):
            v = self.params.getone(self.name)
            v2 = v.split('.')
            v2.reverse()
            return '-'.join(v2)
        else:
            return ''
        
    def render(self, **kwargs):
        value= self._value and self._value or ''
        if value:
            v2 = value.split('-')
            v2.reverse()
            value = ".".join(v2) 
        return h.text_field(self.name, value=str(value), **kwargs)
        
    def render_readonly(self, **kwargs):
        """render html for read only mode"""
        value= self._value and self._value or ''
        if value:
            v2 = value.split('-')
            v2.reverse()
            value = ".".join(v2)
        return value
    
class DateRangeRenderer(FieldRenderer):
    
    def _serialized_value(self):
        if self.params.has_key("%s__von" % self.name):
            von = self.params.getone("%s__von" % self.name)
        else:
            von = ''
        if self.params.has_key("%s__bis" % self.name):
            bis = self.params.getone("%s__bis" % self.name)
        else:
            bis = ''
        #print "%s-->%s" % (von, bis)
        return "%s-->%s" % (von, bis)
        
    def render(self, **kwargs):
        from formalchemy import helpers as h
        value= self._value and self._value or ''
        v = value.split('-->')
#        # print len(v)
        von = ''
        bis = ''
        if len(v) == 2:
            von = v[0]
            bis = v[1]
        kw1 = {'class':'datefrom'}
        kw2 = {'class':'dateuntil'}
        return "%s %s" % (h.text_field("%s__von" % self.name, value=von, **kw1), h.text_field("%s__bis" % self.name, value=bis, **kw2))

class CheckBoxCheckedFieldRenderer(JaNeinRenderer):
    """render a boolean value as checkbox field, but set it to checked, if no value is given"""
    
    def render(self, **kwargs):
        if self.params is None and not self.field.model._sa_instance_state.key: # Default: checked! key enthaelt den Primaeschluessel bei existierenden Objekten
            return h.check_box(self.name, True, checked=True, **kwargs)
        else:
            return CheckBoxFieldRenderer.render(self, **kwargs)
        
class JaNeinRadioSet(RadioSet):
    def render_readonly(self, **kwargs):
        """render html for read only mode"""
        if self._value and self._value == 'True':
            return "Ja"
        else:
            return "Nein"
    
    def _render(self, default=None, **kwargs):
        value = default or self.value
        self.radios = []
        for i, (choice_name, choice_value) in enumerate( [('Ja','True'),('Nein','False')]):
            choice_id = '%s_%i' % (self.name, i)
            radio = self.widget(self.name, choice_value, id=choice_id,
                                checked=self._is_checked(choice_value, value),
                                **kwargs)
            label = h.label(choice_name, for_=choice_id)
            self.radios.append(h.literal(self.format % dict(field=radio,
                                                            label=label)))
        return h.tag("br").join(self.radios)

    def render(self, **kwargs):
        if self.params is None and not self.field.model._sa_instance_state.key: # Default: checked! key enthaelt den Primaeschluessel bei existierenden Objekten
            return self._render(default='False', **kwargs)
        else:
            return self._render(default=None, **kwargs)


class RadioSetChecked(JaNeinRadioSet):
    """render a boolean value as checkbox field, but set it to checked, if no value is given"""
    
    def render(self, **kwargs):
        if self.params is None and not self.field.model._sa_instance_state.key: # Default: checked! key enthaelt den Primaeschluessel bei existierenden Objekten
            return self._render(default='True', **kwargs)
        else:
            return self._render(default=None, **kwargs)


class DefaultStringRenderer(FieldRenderer):
    """
    """
    
    def render_readonly(self, **kwargs):
        """render html for read only mode"""
        value = "FTD2014"
        return value
    
    
FieldSet.default_renderers[type(None)] = NoneRenderer
FieldSet.default_renderers[types.DateTime] = DateTimeAsTextRenderer
FieldSet.default_renderers[types.Date] = DateAsTextRenderer





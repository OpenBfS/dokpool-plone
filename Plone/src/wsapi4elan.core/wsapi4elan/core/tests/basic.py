# -*- coding: utf-8 -*-
from xmlrpclib import ServerProxy
from random import random
def elan_login(username, password):
    return ServerProxy("http://%s:%s@localhost:8081/dokpool" % (username, password), verbose=True)

def getESDs(client):
    """
    Determine all available ESDs, i.e. Top-Level Obects of type ELANESD
    """
    return _queryObjects(client, "/", "DocumentPool")
    
def _queryObjects(client, path, type):
    """
    """
    q = client.query({ 'path': path, 'portal_type': type })
    # print len(q)
    return q.keys()

def _getContents(client, path):
    obj = client.get_object([ path ])
    info = obj.get(path)
    contents = info[2]['contents']
    return contents.keys()

def getTypes(client, esdpath):
    """
    """
    return _queryObjects(client, esdpath, "DocType")

client = elan_login("elanmanager", "admin")
client.get_object()
#q = client.query()
#print len(q)
#print client.get_object(['/Plone/front-page', 'bfs'])

esds = getESDs(client)
print esds
for esdpath in esds:
    ts = getTypes(client, esdpath)
    for t in ts:
        # print t
        o = client.get_object([t])
        # print o
        
print client.get_primary_documentpool()[0]
esdpath = "/dokpool/bund"
group_folders = client.get_group_folders(esdpath)
print group_folders
ufpath = group_folders.keys()[0]
"""
        @param params - dictionary of path with a list value where list item zero are
                        attribute names and their respective values; and list item one
                        is the type name.
                      - { path: [{ attr: value, ...}, type_name], ...}
        =returns [path, ...]
"""
params = { ufpath + "/neue" : [ { "title": "Titel", 
                                   "description" : "Beschreibung",
                                   "text" : "<p>Text</p>",
                                   "docType" : "eventinformation"} , "DPDocument"] }
scenarios = ["demo-am-24-4"]
behaviours = ['elan']
newpath = client.create_dp_document(ufpath, "ganzneues" + str(random() * 100000), "Titel", "Beschreibung", "<p>Neuer Text</p>", "eventinformation", behaviours)
print newpath
params = { "scenarios" : scenarios, "subjects" : ["Henning", "Rietz"] }
client.update_dp_object(newpath, params)

# from xmlrpclib import Binary
# f = open('test.pdf', 'r')
# binary_data = Binary(f.read())
# f.close()
# newfile = client.upload_file(newpath, "datei", "Neue Datei", "Dies ist eine neue Datei", binary_data, "test.pdf")
# f = open('test.jpg', 'r')
# binary_data = Binary(f.read())
# f.close()
# newfile = client.upload_image(newpath, "bild", "Neues Bild", "Dies ist ein neues Bild", binary_data, "text.jpg")

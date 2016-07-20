package de.bfs.elan.client;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.Vector;

import org.apache.xmlrpc.client.XmlRpcClient;
//import redstone.xmlrpc.XmlRpcClient;

import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.apache.commons.io.FileUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import de.bfs.elan.client.Utils;


/**
 * The root class to access XMLRPC services for ELAN-E.
 *
 */
public class DocpoolBaseService {
    private Log log = LogFactory.getLog(DocpoolBaseService.class);
	private XmlRpcClient client = null;
	
	/**
	 * Get a service object.
	 * @param url: the address of the ELAN instance root
	 * @param username
	 * @param password
	 */
	public DocpoolBaseService(String url, String username, String password) {
		XmlRpcClientConfigImpl config = new XmlRpcClientConfigImpl();

		//you can now do authenticated XML-RPC calls with the proxy
	try {
			URL serverurl = new URL(url);
			config.setServerURL(serverurl);
			config.setBasicUserName(username);
			config.setBasicPassword(password);
			client = new XmlRpcClient();
			//concatenate and base64 encode the username and password (suitable for use in HTTP Basic Authentication)
			//final String auth = javax.xml.bind.DatatypeConverter.printBase64Binary((username + ":" + password).getBytes());
			//set the HTTP Header for Basic Authentication
			//client.setRequestProperty("Authorization", "Basic " + auth);
			client.setConfig(config);
			client.setTypeFactory(new DocPoolBaseTypeFactory(client));
		} catch (MalformedURLException e) {
			log.fatal("Incorrect URL provided!", e);
		}
	}

	
	/**
	 * Get all ESDs available to the current user.
	 * @return
	 */
	public List<DocumentPool> getDocumentPools() {
		Map<String, Object> esds = Utils.queryObjects(this.client, "/", "DocumentPool");
		if (esds != null) {
			ArrayList<DocumentPool> res = new ArrayList<DocumentPool>();
			for (String path: esds.keySet()) {
				res.add(new DocumentPool(client, path, null));
			}
			return res;
		} else {
			return null;
		}
	}
	
	/**
	 * @return the ESD, which the user is a member of - or the first available ESD for global users
	 */
	public DocumentPool getPrimaryDocumentPool() {
		Object[] res = (Object[])Utils.execute(client, "get_primary_documentpool", new Vector());
		log.info(res.length);
		return new DocumentPool(client, (String)res[0], (Object[])res[1]);
	}
	
	
	/**
	 * Test method
	 * @param args:unused
	 * @throws IOException 
	 */
	public static void main(String[] args) throws IOException {
	    Log log = LogFactory.getLog(DocpoolBaseService.class);
		
		DocpoolBaseService baseService = new DocpoolBaseService("http://localhost:8081/Plone", "condat_user1", "user1");
		List<DocumentPool> documentpools = baseService.getDocumentPools();
		DocumentPool myDocumentPool = baseService.getPrimaryDocumentPool();
		log.info(myDocumentPool.getTitle());
		log.info(myDocumentPool.getDescription());
		List<DocType> types = myDocumentPool.getTypes();
		for (DocType t : types) {
			log.info(t.getId());
			log.info(t.getTitle());
		}
		Folder userfolder = myDocumentPool.getUserFolder();
		List<Object> documents = userfolder.getContents(null);
		log.info(userfolder.getTitle());
		List<Folder> gf = myDocumentPool.getGroupFolders();
		List<Folder> tf = myDocumentPool.getTransferFolders();
		log.info(gf.size());
		Map<String, Object> properties = new HashMap<String, Object>();
		properties.put("title","Generischer Titel");
		properties.put("description","Generische Beschreibung");
		properties.put("text","<b>Text</b>");
		properties.put("docType","ifinprojection");
		properties.put("scenarios",new String[]{"scenario1","scenario2"});
		properties.put("subjects", new String[]{"Tag1","Tag2"});
		properties.put("local_behaviors", new String[]{"elan"});
		BaseObject bo = userfolder.createObject("generisch9", properties, "DPDocument");
		log.info(bo.getStringAttribute("created_by"));
		log.info(bo.getDateAttribute("effective"));		
		Document d = userfolder.createDocument("ausjava1", "Neu aus Java", "Beschreibung über Java", "<p>Text aus Java!</p>", "ifinprojection", new String[]{"scenario1","scenario2"});
		log.info(d.getTitle());
		java.io.File file = new java.io.File("test.pdf");
		d.uploadFile("neue_datei", "Neue Datei", "Datei Beschreibung", FileUtils.readFileToByteArray(file), "test.pdf");
		file = new java.io.File("test.jpg");
		d.uploadImage("neues_bild", "Neues Bild", "Bild Beschreibung", FileUtils.readFileToByteArray(file), "test.jpg");
		log.info(d.getWorkflowStatus());
		Folder mygf = gf.get(0);
		d = mygf.createDocument("ausjava2", "Neu aus Java", "Beschreibung über Java", "<p>Text aus Java!</p>", "ifinprojection", new String[]{"scenario1","scenario2"});
		log.info(d.getWorkflowStatus());
		d.setWorkflowStatus("publish");
		log.info(d.getWorkflowStatus());
		System.out.println(myDocumentPool.path);
		User user = myDocumentPool.createUser("testuserxml", "testuserxml", "XMLTESTER", myDocumentPool.path);
		if (user == null) {
			log.error("Kein Nutzer angelegt!");
		} else {
			log.info("Nutzer " + user.getUserId() + " angelegt.");
		}
		Group group = myDocumentPool.createGroup("groupxml", "GroupXML", "Fuer XMLRPC",  myDocumentPool.path);
		if (group == null) {
			log.error("Keine Gruppe angelegt.");
		} else {
			log.info("Gruppe " + group.getGroupId() + " angelegt.");
		}
		//user.addToGroup(group);
		group.addUser(user,myDocumentPool.path);
		String[] docTypes = {"airactivity", "ifinprojection", "protectiveactions"};
		group.setAllowedDocTypes(docTypes);
		List<String> gDoctypes = group.getAllowedDocTypes();
		log.info("docTypes " + docTypes);
		log.info("gDocTypes " + gDoctypes);
		if (gDoctypes != null && gDoctypes.equals(Arrays.asList(docTypes))) {
			log.info("Gruppenproperties erfolgreich angepasst.");
		} else {
			log.error("Fehler bei der Anpassung der Gruppenproperties.");
		}
		
	}

}

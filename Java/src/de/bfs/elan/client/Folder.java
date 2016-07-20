package de.bfs.elan.client;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Vector;

import org.apache.xmlrpc.client.XmlRpcClient;

/**
 * Wraps all Folder types and functions as a base class for all folderish types.
 *
 */
public class Folder extends BaseObject {
	protected Map<String,Object> contents = null;
	
	public Folder(XmlRpcClient client, String path, Object[] alldata) {
		super(client, path, alldata);
		if (alldata != null) {
			contents = (Map<String,Object>)((Map<String,Object>)alldata[2]).get("contents");
		}
	}
	
	/**
	 * @return the complete contents of this folder
	 */
	private Map<String,Object> getContents() {
		if (contents == null) {
			contents = (Map<String,Object>)((Map<String,Object>)((Object[])(getObjectData()[1]))[2]).get("contents");
		}
		return contents;
	}
	

	/**
	 * Get a subfolder.
	 * @param subpath: the relative path of the subfolder
	 * @return the subfolder
	 */
	public Folder getFolder(String subpath) {
		Vector<String> params = new Vector<String>();
		params.add(path);
		params.add(subpath);
		Object[] res = (Object[])Utils.execute(client, "get_plone_object", params);
		return new Folder(client, (String)res[0], (Object[])res[1]);
	}
	
	/**
	 * Return all folder contents, can be filtered by type.
	 * @param type: the Plone type name or null
	 * @return folder contents, possibly filtered by type
	 */
	public List<Object> getContents(String type) {
		if (getContents() != null) {
			ArrayList<Object> res = new ArrayList<Object>();
			for (String path: getContents().keySet()) {
				Map<String,Object> metadata = (Map<String,Object>)contents.get(path);
				String portal_type = (String)metadata.get("Type");
				if ((type == null) || (type.equals(portal_type))) {
					if (portal_type.equals("SimpleFolder") || portal_type.equals("ELANTransferFolder")) {
						res.add(new Folder(client, path, null));
					} else if (portal_type.equals("DPDocument") || portal_type.equals("InfoDocument")) {
						res.add(new Document(client, path, null));
					} else if (portal_type.equals("File")) {
						res.add(new File(client, path, null));
					} else if (portal_type.equals("Image")) {
						res.add(new Image(client, path, null));
					}
				}
			}
			return res;
		} else {
			return null;
		}
		
	}
	
	/**
	 * @return only subfolders of type ELANFolder
	 */
	public List<Object> getSubFolders() {
		return getContents("SimpleFolder");
	}
	
	/**
	 * @return only documents within this folder
	 */
	public List<Object> getDocuments() {
		return getContents("DPDocument");
	}
	
	/**
	 * Create a new document within this folder.
	 * 
	 * @param id: the short name for the document (must be unique within the folder) 
	 * @param title
	 * @param description
	 * @param text
	 * @param docType
	 * @param scenario
	 * @return the newly created document
	 */
	public Document createDocument(String id, String title, String description, String text, String docType, String[] scenarios) {
		Map<String, Object> properties = new HashMap<String, Object>();
		properties.put("title",title);
		properties.put("description",description);
		properties.put("text",text);
		properties.put("docType",docType);
		properties.put("scenarios",scenarios);
		return createDocument(id, properties);
	}
	
	public Document createDocument(String id, Map<String, Object> properties) {
		Vector<Object> params = new Vector<Object>();
		params.add(path);
		params.add(id);
		params.add(properties);
		params.add("DPDocument");
		String newpath = (String)execute("create_dp_object", params);
		return new Document(client, newpath, null);		
	}

	public BaseObject createObject(String id, Map<String, Object> properties, String type) {
		Vector<Object> params = new Vector<Object>();
		params.add(path);
		params.add(id);
		params.add(properties);
		params.add(type);
		String newpath = (String)execute("create_dp_object", params);
		return new BaseObject(client, newpath, null);		
	}
	
	
}

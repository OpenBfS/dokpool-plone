package de.bfs.elan.client;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.Vector;

import org.apache.xmlrpc.client.XmlRpcClient;


/**
 * Base class for all API objects. Contains helper methods for all types.
 *
 */
class BaseObject {
	protected XmlRpcClient client = null;
	protected String path = null;
	protected Map<String,Object> data = null;
	protected Map<String,Object> metadata = null;
	
	protected BaseObject(XmlRpcClient client, String path, Object[] alldata) {
		this.client = client;
		this.path = path;
		if (alldata != null) {
			data = (Map<String,Object>)alldata[0];
		}
	}
	

	/**
	 * Fetches all data and contents for this object via XMLRPC.
	 * @return object data as XMLRPC structure
	 */
	protected Object[] getObjectData() {
		Vector<String> params = new Vector<String>();
		params.add(path);
		params.add("");
		Object[] res = (Object[])execute("get_plone_object", params);
		return res;
	}
	
	/**
	 * Gets just the attributes for the object from XMLRPC data.
	 * @return object attributes as map
	 */
	private Map<String,Object> getData() {
		if (data == null) {
			data = (Map<String,Object>)((Object[])(getObjectData()[1]))[0];
		}
		return data;
	}
	
	
	protected Object execute(String command, Vector params) {
		return Utils.execute(this.client, command, params);
	}
	
	/**
	 * Helper to get value of a string valued attribute.
	 * @param name: the name of the attribute
	 * @return the String value
	 */
	public String getStringAttribute(String name) {
		if (getData() != null) {
			return (String)getData().get(name);			
		}
		else {
			return null;
		}
	}
	
	public Date getDateAttribute(String name) {
		if (getData() != null) {
			return (Date)getData().get(name);			
		}
		else {
			return null;
		}		
	}
	
	public String getId() {
		return getStringAttribute("id");
	}
		
	public String getTitle() {
		return getStringAttribute("title");
	}
	
	public String getDescription() {
		return getStringAttribute("description");
	}
	
	
	/**
	 * @return The workflow status of the object (i.e. 'published', 'private', ...)
	 */
	public String getWorkflowStatus() {
		Vector<String> params = new Vector<String>();
		params.add(path);
		Map<String, Object> res = (Map<String, Object>)execute("get_workflow", params);
		return (String)res.get("state");
	}
	
	/**
	 * Attempts to execute a transition to set a new workflow status.
	 * @param transition: the name of the transition
	 */
	public void setWorkflowStatus(String transition) {
		Vector<String> params = new Vector<String>();
		params.add(transition);
		params.add(path);
		execute("set_workflow", params);		
	}
	
	
}

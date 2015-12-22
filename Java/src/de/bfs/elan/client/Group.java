package de.bfs.elan.client;

import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.Vector;

import org.apache.xmlrpc.client.XmlRpcClient;

public class Group extends BaseObject {
	
	private String groupId = "";
	private String dp = "";
	private String title = "";
	private String description = "";
	private Set<User> members = new HashSet<User>();
	private List<String> allowedDocTypes;
	
	protected Group(XmlRpcClient client, String path, String groupId, String title, String description, String dp) {
		super(client, path, null);
		this.groupId = groupId;
		this.title = title;
		this.description = description;
		this.dp = dp;
	}

	public void setAllowedDocTypes(String[] doctypes) {
		Vector<Object> params = new Vector<Object>();
		params.add(groupId);
		params.add(title);
		params.add(description);
		params.add(dp);
		params.add(doctypes);
		Object o = execute("put_group", params);
		if (((String) o).equals("changed")) {
			allowedDocTypes = Arrays.asList(doctypes);
		}
	}
	
	public void addUser(User user,String esd) {
		Vector<String> params = new Vector<String>();
		params.add(user.getUserId());
		params.add(groupId);
		params.add(esd);
		Object o = execute("add_user_to_group", params);
		if (((String) o).equals("added")) {
			members.add(user);
		}
		
	}
	
	public String getGroupId() {
		return groupId;
	}
	
	public String getEsd() {
		return dp;
	}
	
	public String getTitle() {
		return title;
	}
	
	public String getDescription() {
		return description;
	}

	public List<String> getAllowedDocTypes() {
		return allowedDocTypes;
	}

}
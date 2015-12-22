package de.bfs.elan.client;

import java.util.Vector;

import org.apache.xmlrpc.client.XmlRpcClient;

public class User extends BaseObject{
	private String userId = "";
	private String fullname = "";
	private String dp = "";
	
	protected User(XmlRpcClient client, String path, String userId, String password, String fullname, String dp) {
		super(client, path, null);
		this.userId = userId;
		this.fullname = fullname;
		this.dp = dp;
	}
	
	public void addToGroup(Group group) {
		/*Vector<String> params = new Vector<String>();
		params.add(this.userId);
		params.add(group.getGroupId());
		Object o = execute("add_user_to_group", params);*/
		group.addUser(this,this.path);
	}
	
	public String getUserId() {
		return this.userId;
	}
	
	public String getFullname() {
		return this.fullname;
	}
	
	public String getEsd() {
		return  this.dp;
	}
}
/**
 * 
 */
package de.bfs.elanadmin;

/**
 * @author Peter Bieringer
 * @version 1.0
 * 
 *         Class for the user information
 *
 */
public class user {

	private String fullname;
	private String userId;
	private String password;
	private String esd;

	/**
	 * @param fullname
	 * @param userId
	 * @param password
	 * @param esd
	 */
	public user(String fullname, String userId, String password, String esd) {
		super();
		this.fullname = fullname;
		this.userId = userId;
		this.password = password;
		this.esd = esd;
	}

	public String getFullname() {
		return fullname;
	}

	public void setFullname(String fullname) {
		this.fullname = fullname;
	}

	public String getUserId() {
		return userId;
	}

	public void setUserId(String userId) {
		this.userId = userId;
	}

	public String getPassword() {
		return password;
	}

	public void setPassword(String password) {
		this.password = password;
	}

	public String getEsd() {
		return esd;
	}

	public void setEsd(String esd) {
		this.esd = esd;
	}

	@Override
	public String toString() {
		return "user [fullname=" + fullname + ", userId=" + userId
				+ ", password=" + password + ", esd=" + esd + "]";
	}

}

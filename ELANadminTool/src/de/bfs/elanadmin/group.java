/**
 * 
 */
package de.bfs.elanadmin;

import java.util.Arrays;

/**
 * @author Peter Bieringer
 * @version 1.0
 * 
 *         Class for the group information
 *
 */
public class group {

	private String groupId;
	private String title;
	private String desc;
	private String esd;
	private String[] allowedDoctypes;
	private String[] members;

	/**
	 * @param groupId
	 * @param title
	 * @param desc
	 * @param esd
	 * @param allowedDoctypes
	 * @param members
	 */
	public group(String groupId, String title, String desc, String esd,
			String[] allowedDoctypes, String[] members) {
		super();
		this.groupId = groupId;
		this.title = title;
		this.desc = desc;
		this.esd = esd;
		this.allowedDoctypes = allowedDoctypes;
		this.members = members;
	}

	public String getGroupId() {
		return groupId;
	}

	public void setGroupId(String groupId) {
		this.groupId = groupId;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public String getDesc() {
		return desc;
	}

	public void setDesc(String desc) {
		this.desc = desc;
	}

	public String getEsd() {
		return esd;
	}

	public void setEsd(String esd) {
		this.esd = esd;
	}

	public String[] getAllowedDoctypes() {
		return allowedDoctypes;
	}

	public void setAllowedDoctypes(String[] allowedDoctypes) {
		this.allowedDoctypes = allowedDoctypes;
	}

	public String[] getMembers() {
		return members;
	}

	public void setMembers(String[] members) {
		this.members = members;
	}

	@Override
	public String toString() {
		return "group [groupId=" + groupId + ", title=" + title + ", desc="
				+ desc + ", esd=" + esd + ", allowedDoctypes="
				+ Arrays.toString(allowedDoctypes) + ", members="
				+ Arrays.toString(members) + "]";
	}

}

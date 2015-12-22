package de.bfs.elanadmin;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.MissingResourceException;
import java.util.ResourceBundle;

import de.bfs.elan.client.DocpoolBaseService;
import de.bfs.elan.client.DocumentPool;
import de.bfs.elan.client.Group;
import de.bfs.elan.client.User;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

/**
 * @author Peter Bieringer
 * @version 1.0
 * 
 *         class for creating groups and users in an esd. The information for
 *         this will be read from csv files
 * 
 */

public class UserGroups {

	String esd;
	String fileGroup;
	String fileUser;

	private Log log = LogFactory.getLog(UserGroups.class);

	/**
	 * @param esd
	 * @param fileGroup
	 * @param fileUser
	 */
	public UserGroups(String esd, String fileGroup, String fileUser) {
		super();
		this.esd = esd;
		this.fileGroup = fileGroup;
		this.fileUser = fileUser;

		List<user> u;
		List<group> g;

		u = readUsers(fileUser);
		g = readGroups(fileGroup);

		// connect to wsapi
		// read host, port, user etc from the properties file
		ResourceBundle resources;

		try {
			resources = ResourceBundle.getBundle("resources.ElanadminClient",
					Locale.getDefault());

			String host = resources.getString("HOST");
			String port = resources.getString("PORT");
			String ploneSite = resources.getString("PLONE_SITE");
			String user = resources.getString("USER");
			String pw = resources.getString("PW");

			DocpoolBaseService dp = new DocpoolBaseService("http://" + host
					+ ":" + port + "/" + ploneSite, user, pw);
			DocumentPool mydp = dp.getPrimaryDocumentPool();
			log.info("You are connected to " + mydp.getTitle());

			int i = 0;

			List<User> member = new ArrayList<User>();
			// create users from list
			for (i = 0; i < u.size(); i++) {
				System.out.println(u.get(i).toString());
				User ben = mydp.createUser(u.get(i).getUserId(), u.get(i)
						.getPassword(), u.get(i).getFullname(), u.get(i)
						.getEsd());

				if (ben == null) {
					log.error("No user created!");
				} else {
					log.info("User " + ben.getUserId() + " created.");
					member.add(ben);
				}
			}

			// create groups from list
			for (i = 0; i < g.size(); i++) {
				System.out.println(g.get(i).toString());
				Group group = mydp.createGroup(g.get(i).getGroupId(), g.get(i)
						.getTitle(), g.get(i).getDesc(), g.get(i).getEsd());
				if (group == null) {
					log.error("No group created!");
				} else {
					log.info("Group " + group.getGroupId() + " created.");
					// allowed Doctypes
					group.setAllowedDocTypes(g.get(i).getAllowedDoctypes());

					// add users
					String[] m = g.get(i).getMembers();
					for (int ii = 0; ii < m.length; ii++) {
						for (int iii = 0; iii < member.size(); iii++) {
							if (member.get(iii).getUserId().equals(m[ii]))
								group.addUser(member.get(iii), g.get(i)
										.getEsd());
						}

					}
				}
			}
		} catch (MissingResourceException mre) {
			System.err
					.println("resources/ElanadminClient.properties not found");
			System.exit(-1);
		}

	}

	/**
	 * @param filename
	 * @return
	 */
	private List<user> readUsers(String filename) {
		List<user> users = new ArrayList<user>();
		BufferedReader bri = null;

		String buf = new String();

		try {
			bri = new BufferedReader(new FileReader(filename));
		} catch (FileNotFoundException fnfe) {
			System.err.println("File " + filename + " not found: " + fnfe);
			System.exit(0);
		}

		try {
			String line[];

			// read all -> no headline

			while ((buf = bri.readLine()) != null) {
				line = decodeLine(buf);

				try {
					user u = new user(line[0], line[1], line[2], esd);

					
					users.add(u);
				} catch (Exception e) {
					for (int ii = 0; ii < line.length; ii++)
						System.out.println(ii + " [" + line[ii] + "] ");
				}
			}
			bri.close();
			
			return users;
		} catch (IOException io) {
			System.out.println("Fehler beim Lesen!" + io);
		}

		return users;

	}

	/**
	 * @param filename
	 * @return
	 */
	private List<group> readGroups(String filename) {
		List<group> groups = new ArrayList<group>();
		BufferedReader bri = null;

		String buf = new String();

		try {
			bri = new BufferedReader(new FileReader(filename));
		} catch (FileNotFoundException fnfe) {
			System.err.println("File " + filename + " not found: " + fnfe);
			System.exit(0);
		}

		try {
			String line[];

			// read all  -> no headline

			while ((buf = bri.readLine()) != null) {
				line = decodeLine(buf);

				try {
					group g = new group(line[0], line[1], "demo1", esd,
							decodePart(line[2]), decodePart(line[3]));
					
					groups.add(g);
				} catch (Exception e) {
					for (int ii = 0; ii < line.length; ii++)
						System.out.println(ii + " [" + line[ii] + "] ");
				}
			}
			bri.close();
			
			return groups;
		} catch (IOException io) {
			System.out.println("Fehler beim Lesen!" + io);
		}

		return groups;
	}

	/**
	 * splits string to array of strings - delimiter ";"
	 */
	private String[] decodeLine(String zeile) {
		return zeile.split(";");
	}

	/**
	 * splits string to array of strings - delimiter ","
	 */
	private String[] decodePart(String zeile) {
		return zeile.split(",");
	}

	public static void main(String[] args) {

		if (args.length < 3) {
			System.out
					.println(args.length
							+ "cmd: java UserGroups <full path to ESD> <filename groups> <filename users>");
			System.exit(-1);
		} else {
			UserGroups ug = new UserGroups(args[0], args[1], args[2]);
		}

	}

}

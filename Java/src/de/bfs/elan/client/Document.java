package de.bfs.elan.client;

import java.util.Vector;

import org.apache.xmlrpc.client.XmlRpcClient;

/**
 * Wraps the ELANDocument type
 *
 */
public class Document extends Folder {
	public Document(XmlRpcClient client, String path, Object[] data) {
		super(client, path, data);
	}
	
	/**
	 * Uploads a file into the document
	 * @param id: short name for the file
	 * @param title
	 * @param description
	 * @param data: binary data of the file
	 * @param filename
	 * @return
	 */
	public File uploadFile(String id, String title, String description, byte[] data, String filename) {
		Vector<Object> params = new Vector<Object>();
		System.out.println("Dokument: "+id+title+description+filename);
		params.add(path);
		params.add(id);
		params.add(title);
		params.add(description);
		params.add(data);
		params.add(filename);
		String newpath = (String)execute("upload_file", params);
		return new File(client, newpath, null);
	}

	/**
	 * Uploads an image into the document
	 * @param id: short name for the image
	 * @param title
	 * @param description
	 * @param data: binary data of the image
	 * @param filename
	 * @return
	 */	public Image uploadImage(String id, String title, String description, byte[] data, String filename) {
		Vector<Object> params = new Vector<Object>();
		System.out.println("Dokument: "+id+title+description+filename);
		params.add(path);
		params.add(id);
		params.add(title);
		params.add(description);
		params.add(data);
		params.add(filename);
		String newpath = (String)execute("upload_image", params);
		return new Image(client, newpath, null);
	}
	public String autocreateSubdocuments() {
		Vector<Object> params = new Vector<Object>();
		params.add(path);
		String msg = (String)execute("autocreate_subdocuments", params);
		return msg;
	 }
	 
	 public String readPropertiesFromFile() {
		Vector<Object> params = new Vector<Object>();
		params.add(path);
		String msg = (String)execute("read_properties_from_file", params);
		return msg;
	 }

}

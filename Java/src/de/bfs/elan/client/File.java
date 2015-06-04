package de.bfs.elan.client;

import org.apache.xmlrpc.client.XmlRpcClient;

/**
 * Wraps the Plone File object.
 *
 */
public class File extends BaseObject {
	public File(XmlRpcClient client, String path, Object[] data) {
		super(client, path, data);
	}

}

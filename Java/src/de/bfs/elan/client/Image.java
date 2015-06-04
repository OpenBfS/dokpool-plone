package de.bfs.elan.client;

import org.apache.xmlrpc.client.XmlRpcClient;

/**
 * Wraps the Plone Image type
 *
 */
public class Image extends BaseObject {
	public Image(XmlRpcClient client, String path, Object[] data) {
		super(client, path, data);
	}
}

from plone import api
from plone.app.contenttypes.behaviors.collection import ICollection
from Products.Five import BrowserView


class NavigationHelper(BrowserView):
    def number_of_children(self, item):
        """Preview the number of results for each item in the navigation-portlet."""
        collection_types = [
            "ELANDocCollection",
            "DashboardCollection",
            "Collection",
        ]
        folder_types = [
            "Folder",
            "FolderBase",
            "CollaborationFolder",
            "DPTransferFolder",
            "GroupFolder",
            "UserFolder",
            "SimpleFolder",
            "InfoFolder",
            "ELANInfos",
        ]

        # For collections we get the results
        if item["portal_type"] in collection_types:
            collection = item["item"].getObject()
            results = collection.results()
            if not results:
                return None
            results_length = results.sequence_length
            if results_length == ICollection(collection).limit:
                return f"{results_length}+"
            return results_length or None

        # For content we can query the catalog for DPDocuments
        if item["portal_type"] in folder_types:
            brains = api.content.find(
                path={"query": item["path"], "depth": -1},
                portal_type=["DPDocument"],
            )
            return len(brains) or None

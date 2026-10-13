from zope.component import adapter
from zope.interface import Interface
from zope.traversing.interfaces import IBeforeTraverseEvent

import socket


@adapter(Interface, IBeforeTraverseEvent)
def add_backend_header(context, event):
    """Add an HTTP header X-Backend that exports the current hostname.

    This is used by varnish to implement sticky sessions with a dynamic set of backends.

    To work in a container compose environment, the varnish configuration uses a dynamic director to collect
    available backends. Backend multiplicity in this setup is DNS-based, so backends are identified either by
    the generic hostname that is resolved to multiple addresses by compose, or by their unique container names
    or hostnames (which is not the same, and which can only be known at runtime). However, neither these
    unique names nor IP addresses can be retrieved from the VCL backend objects created by the dynamic
    director. Such a unique identifier is, however, required in order to select the same backend on the next
    request of the session. The workaround is for backends to report their identity via an HTTP header that
    can be evaluated in VCL. The round-trip of the value is then achieved via a cookie.

    There are alternatives that don't require app support but somehow need to query the container composer for
    the set of backends. The solution implemented here seems to be more robust than that.
    """
    event.request.response.setHeader("X-Backend", socket.gethostname())

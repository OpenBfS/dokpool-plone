# VCL file optimized for plone.app.caching.  See vcl(7) for details
vcl 4.0;
import directors;
import std;
# This is an example of a split view caching setup with another proxy
# like Apache in front of Varnish to rewrite urls into the VHM style.

# Also assumes a single backend behind Varnish (which could be a single
# zope instance or a load balancer serving multiple zeo clients).
# To change this to support multiple backends, see the vcl man pages
# for instructions.


backend b1 {
    .host = "${hosts:instance1}";
    .port = "${ports:instance1}";
    .probe = { .url = "/"; .interval = 30s; .timeout = 20s; .window = 6; .threshold = 6; }
    .connect_timeout = 6s;
    .first_byte_timeout = 300s;
    }
backend b2 {
    .host = "${hosts:instance2}";
    .port = "${ports:instance2}";
    .probe = { .url = "/"; .interval = 30s; .timeout = 20s; .window = 6; .threshold = 6; }
    .connect_timeout = 6s;
    .first_byte_timeout = 300s;
    }
backend b3 {
    .host = "${hosts:instance3}";
    .port = "${ports:instance3}";
    .probe = { .url = "/"; .interval = 30s; .timeout = 20s; .window = 6; .threshold = 6; }
    .connect_timeout = 6s;
    .first_byte_timeout = 300s;
    }
backend b4 {
    .host = "${hosts:instance4}";
    .port = "${ports:instance4}";
    .probe = { .url = "/"; .interval = 30s; .timeout = 20s; .window = 6; .threshold = 6; }
    .connect_timeout = 6s;
    .first_byte_timeout = 300s;
     }
backend b5 {
    .host = "${hosts:instance5}";
    .port = "${ports:instance5}";
    .probe = { .url = "/"; .interval = 30s; .timeout = 20s; .window = 6; .threshold = 6; }
    .connect_timeout = 6s;
    .first_byte_timeout = 300s;
     }
backend b6 {
    .host = "${hosts:instance6}";
    .port = "${ports:instance6}";
    .probe = { .url = "/"; .interval = 30s; .timeout = 20s; .window = 6; .threshold = 6; }
    .connect_timeout = 6s;
    .first_byte_timeout = 300s;
     }
backend b7 {
    .host = "${hosts:instance7}";
    .port = "${ports:instance7}";
    .probe = { .url = "/"; .interval = 30s; .timeout = 20s; .window = 6; .threshold = 6; }
    .connect_timeout = 6s;
    .first_byte_timeout = 300s;
     }
backend b8 {
    .host = "${hosts:instance8}";
    .port = "${ports:instance8}";
    .probe = { .url = "/"; .interval = 30s; .timeout = 20s; .window = 6; .threshold = 6; }
    .connect_timeout = 6s;
    .first_byte_timeout = 300s;
     }

# Only allow PURGE from localhost
acl purge {
    "${hosts:allow-purge}";
}

# Round-robin load balancing between four instances
sub vcl_init {
    new cluster1 = directors.round_robin();
    cluster1.add_backend(b1);
    cluster1.add_backend(b2);
    cluster1.add_backend(b3);
    cluster1.add_backend(b4);
    cluster1.add_backend(b5);
    cluster1.add_backend(b6);
    cluster1.add_backend(b7);
    cluster1.add_backend(b8);
}

sub vcl_hit {
    if (obj.ttl >= 0s) {
        # normal hit
        return (deliver);
    }
    # We have no fresh fish. Lets look at the stale ones.
    if (std.healthy(req.backend_hint)) {
        # Backend is healthy. Limit age to 10s.
        if (obj.ttl + 10s > 0s) {
            set req.http.grace = "normal(limited)";
            return (deliver);
        } else {
            # No candidate for grace. Fetch a fresh object.
            return(miss);
        }
    } else {
        # backend is sick - use full grace
        if (obj.ttl + obj.grace > 0s) {
            set req.http.grace = "full";
            return (deliver);
        } else {
            # no graced object.
            return (miss);
        }
    }
}

sub vcl_recv {
    set req.http.grace = "none";
    set req.backend_hint = cluster1.backend();

    if (req.method == "PURGE") {
        if (!client.ip ~ purge) {
            return(synth(405,"Not allowed."));
        }
        return(purge);
    }
    if (req.method != "GET" && req.method != "HEAD") {
        # We only deal with GET and HEAD by default
        return(pass);
    }
    call normalize_accept_encoding;
    call annotate_request;
    return(hash);
}

sub vcl_backend_response {
    #set beresp.ttl = 10s;
    set beresp.grace = 30m;
    if (beresp.uncacheable) {
        set beresp.http.X-Varnish-Action = "FETCH (pass - not cacheable)";
        return(pass);
    }
    if (beresp.http.Set-Cookie) {
        set beresp.http.X-Varnish-Action = "FETCH (pass - response sets cookie)";
        return(pass);
    }
    if (!beresp.http.Cache-Control ~ "s-maxage=[1-9]" && beresp.http.Cache-Control ~ "(private|no-cache|no-store)") {
        set beresp.http.X-Varnish-Action = "FETCH (pass - response sets private/no-cache/no-store token)";
        return(pass);
    }
    if (!bereq.http.X-Anonymous && !beresp.http.Cache-Control ~ "public") {
        set beresp.http.X-Varnish-Action = "FETCH (pass - authorized and no public cache control)";
        return(pass);
    }
    if (bereq.http.X-Anonymous && !beresp.http.Cache-Control) {
        set beresp.ttl = 10s;
        set beresp.http.X-Varnish-Action = "FETCH (override - backend not setting cache control)";
    } else {
        set beresp.http.X-Varnish-Action = "FETCH (deliver)";
    }
    call rewrite_s_maxage;
    call compress_content;
    return(deliver);
}

sub vcl_deliver {
    call rewrite_age;
    set resp.http.grace = req.http.grace;
}


##########################
#  Helper Subroutines
##########################

# Optimize the Accept-Encoding variant caching
sub normalize_accept_encoding {
    if (req.http.Accept-Encoding) {
        if (req.url ~ "\.(jpe?g|png|gif|swf|pdf|gz|tgz|bz2|tbz|zip)$" || req.url ~ "/image_[^/]*$") {
            unset req.http.Accept-Encoding;
        } elsif (req.http.Accept-Encoding ~ "gzip") {
            set req.http.Accept-Encoding = "gzip";
        } else {
            unset req.http.Accept-Encoding;
        }
    }
}

# Keep auth/anon variants apart if "Vary: X-Anonymous" is in the response
sub annotate_request {
    if (!(req.http.Authorization || req.http.cookie ~ "(^|.*; )__ac=" || req.http.X-SHIB-USER)) {
        set req.http.X-Anonymous = "True";
    }
}

# The varnish response should always declare itself to be fresh
sub rewrite_age {
    if (resp.http.Age) {
        set resp.http.X-Varnish-Age = resp.http.Age;
        set resp.http.Age = "0";
    }
}

# Rewrite s-maxage to exclude from intermediary proxies
# (to cache *everywhere*, just use 'max-age' token in the response to avoid this override)
sub rewrite_s_maxage {
    if (beresp.http.Cache-Control ~ "s-maxage") {
        set beresp.http.Cache-Control = regsub(beresp.http.Cache-Control, "s-maxage=[0-9]+", "s-maxage=0");
    }
}

# Compress content if not done by backend
sub compress_content {
    if (beresp.http.content-type ~ "text") {
        set beresp.do_gzip = true;
    }
}

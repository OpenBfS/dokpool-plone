#This file is only needed for BfS-IMIS-Stack
ARG VARNISH_VERSION
FROM varnish:${VARNISH_VERSION}

# set the user to root
USER root
USER varnish
COPY varnish.vcl /etc/varnish/default.vcl
COPY varnish-build/healthcheck.sh ./
HEALTHCHECK --interval=10s CMD ./healthcheck.sh

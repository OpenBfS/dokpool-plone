FROM varnish:7.1

# set the user to root, and install build dependencies
USER root
RUN set -e; \
    apt-get update; \
    apt-get -y install $VMOD_DEPS /pkgs/*.deb; \
    # install one, possibly multiple vmods
    install-vmod https://github.com/varnish/varnish-modules/releases/download/0.20.0/varnish-modules-0.20.0.tar.gz; \
    # clean up and set the user back to varnish
    apt-get -y purge --auto-remove $VMOD_DEPS varnish-dev; \
    rm -rf /var/lib/apt/lists/*
USER varnish
COPY varnish.vcl_example /etc/varnish/default.vcl
COPY healthcheck.sh ./
HEALTHCHECK --interval=10s CMD ./healthcheck.sh

FROM varnish:7.6

# set the user to root
USER root
USER varnish
COPY varnish.vcl_example /etc/varnish/default.vcl
COPY healthcheck.sh ./
HEALTHCHECK --interval=10s CMD ./healthcheck.sh

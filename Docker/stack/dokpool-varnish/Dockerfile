FROM varnish:7.5


USER root
RUN mkdir /usr/local/varnish

COPY varnish.vcl /usr/local/varnish/
COPY setup_config.sh /usr/local/bin/
RUN rm -f /etc/varnish/default.vcl

RUN ln -s /usr/local/varnish/varnish.vcl /etc/varnish/default.vcl

RUN chown -R varnish:varnish /usr/local/varnish

USER varnish

ENTRYPOINT ["/usr/local/bin/setup_config.sh"]

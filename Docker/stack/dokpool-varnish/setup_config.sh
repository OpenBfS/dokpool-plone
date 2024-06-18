#!/bin/bash

for i in $(seq 1 ${VARNISH_BACKEND_COUNT});
do
if [ ! -f /usr/local/varnish/backend.config ]; then
  cat << EOF >> /usr/local/varnish/backend.cfg
    backend dokpool${i}  {
    .host = "${VARNISH_BACKEND_HOST}_${i}";
    .port = "${VARNISH_BACKEND_PORT}";
    .probe = { .url = "/"; .interval = 30s; .timeout = 20s; .window = 6; .threshold = 6; }
    .connect_timeout = 6s;
    .first_byte_timeout = 300s;
    } 
EOF
else
  cat << EOF > /usr/local/varnish/backend.cfg
    backend dokpool${i} {
    .host = "${VARNISH_BACKEND_HOST}_${i}";
    .port = "${VARNISH_BACKEND_PORT}";
    .probe = { .url = "/"; .interval = 30s; .timeout = 20s; .window = 6; .threshold = 6; }
    .connect_timeout = 6s;
    .first_byte_timeout = 300s;
    }
EOF
fi
done

sed -i '/#reservedForBackend/r /usr/local/varnish/backend.cfg' /usr/local/varnish/varnish.vcl

for i in $(seq 1  ${VARNISH_BACKEND_COUNT});
do
if [ ! -f /usr/local/varnish/loadBalancer.cfg ]; then
  echo "cluster_loadbalancer.add_backend(dokpool${i});" > /usr/local/varnish/loadBalancer.cfg 
else
  echo "cluster_loadbalancer.add_backend(dokpool${i});" >> /usr/local/varnish/loadBalancer.cfg
fi
 
#sub vcl_init {
#  new cluster_loadbalancer = directors.round_robin();
#  cluster_loadbalancer.add_backend(traefik_loadbalancer);
#}
done

sed -i '/#reservedForLBconfig/r /usr/local/varnish/loadBalancer.cfg' /usr/local/varnish/varnish.vcl

exec /usr/local/bin/docker-varnish-entrypoint

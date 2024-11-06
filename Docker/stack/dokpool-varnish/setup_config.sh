#!/bin/bash

if [[ ! -e /usr/local/varnish/backend.cfg ]]; then

for i in $(seq 1 ${VARNISH_BACKEND_COUNT});
do
  cat << EOF >> /usr/local/varnish/backend.cfg
    backend dokpool${i} {
    .host = "${VARNISH_BACKEND_HOST}_${i}";
    .port = "${VARNISH_BACKEND_PORT}";
    .probe = { .url = "/"; .interval = 30s; .timeout = 20s; .window = 6; .threshold = 6; }
    .connect_timeout = 6s;
    .first_byte_timeout = 300s;
    }
EOF
done
sed -i '/#reservedForBackend/r /usr/local/varnish/backend.cfg' /usr/local/varnish/varnish.vcl
fi

if [[ ! -e /usr/local/varnish/loadBalancer.cfg ]]; then

  for i in $(seq 1  ${VARNISH_BACKEND_COUNT});
   do
   echo "cluster_loadbalancer.add_backend(dokpool${i});" >> /usr/local/varnish/loadBalancer.cfg
  done
  sed -i '/#reservedForLBconfig/r /usr/local/varnish/loadBalancer.cfg' /usr/local/varnish/varnish.vcl
fi


exec /usr/local/bin/docker-varnish-entrypoint

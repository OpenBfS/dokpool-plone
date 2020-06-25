// TODO expose-loader can be updated to 1.0.0 - not yet done
// https://github.com/webpack-contrib/expose-loader/blob/master/CHANGELOG.md#100-2020-06-23
import "expose-loader?OpenLayers!exports-loader?OpenLayers!OpenLayers";
import(/* webpackChunkName: "proj4" */ 'proj4');
import(/* webpackChunkName: "collectivegeo_init" */ 'collectivegeo_init');
import(/* webpackChunkName: "collectivegeo" */ 'collectivegeo')
import("++plone++openlayers.static/openlayers/theme/default/style.css");
import("++plone++openlayers.static/openlayers/theme/default/google.css");
import("++plone++openlayers.static/geo-openlayers.css");
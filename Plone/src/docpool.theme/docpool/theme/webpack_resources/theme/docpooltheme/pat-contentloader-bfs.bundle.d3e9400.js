(window.webpackJsonp=window.webpackJsonp||[]).push([[13],{29:function(t,e,n){n.e(19).then((function(){var t=[n(0),n(49),n(4),n(2),n(51),n(1)];(function(t,e,n,o,l,s){"use strict";var a=n.getLogger("pat-contentloader-bfs");return e.extend({name:"contentloader-bfs",trigger:".pat-contentloader-bfs",parser:"mockup",defaults:{url:null,content:null,trigger:"click",target:null,template:null,dataType:"html"},init:function(){var t=this;"el"===t.options.url&&"A"===t.$el[0].tagName&&(t.options.url=t.$el.attr("href")),t.$el.removeClass("loading-content"),t.$el.removeClass("content-load-error"),"immediate"===t.options.trigger?t._load():t.$el.on(t.options.trigger,(function(e){e.preventDefault(),t._load()}))},_load:function(){this.$el.addClass("loading-content"),this.$el.toggleClass("close");var t=this.$el.parent().find("a").not(".loading-content");t!=this.$el&&t.hasClass("close")&&t.removeClass("close");var e=this.$el.closest("tr").next("tr");e.hasClass("target_open")?e.remove():this.options.url?this.loadRemote():this.loadLocal()},loadRemote:function(){var e=this;t.ajax({url:e.options.url,dataType:e.options.dataType,success:function(n){var o;if("html"===e.options.dataType)-1!==n.indexOf("<html")&&(n=l.parseBodyTag(n)),o=t('<tr class="target_open"><td>&nbsp</td><td>&nbsp</td> <td>&nbsp</td><td colspan="3">'+n+"</td> <td>&nbsp</td> <td>&nbsp</td></tr>");else if(-1!==e.options.dataType.indexOf("json")){n.constructor===Array&&1===n.length&&(n=n[0]);try{o=t(s.template(e.options.template)(n))}catch(t){return e.$el.removeClass("loading-content"),e.$el.addClass("content-load-error"),void a.warn("error rendering template. pat-contentloader will not work")}}null!==e.options.content&&(o=o.find(e.options.content)),e.loadLocal(o)},error:function(){e.$el.removeClass("loading-content"),e.$el.addClass("content-load-error")}})},loadLocal:function(e){if(!e&&null===this.options.content)return this.$el.removeClass("loading-content"),this.$el.addClass("content-load-error"),void a.warn("No selector configured");var n=this.$el;if(null!==this.options.target&&0===(n=t(this.options.target)).size())return this.$el.removeClass("loading-content"),this.$el.addClass("content-load-error"),void a.warn("No target nodes found");if(!e){var l=t(this.options.content).clone();e=t('<tr class="target_open"><td>&nbsp</td><td>&nbsp</td> <td>&nbsp</td><td colspan="3"><h4>'+l.text()+"</h4></td> <td>&nbsp</td> <td>&nbsp</td></tr>")}n=n.closest("tr"),e.length?(e.show(),n.after(e),o.scan(e)):n.empty(),this.$el.removeClass("loading-content"),this.emit("loading-done")}})}).apply(null,t)})).catch(n.oe)}}]);
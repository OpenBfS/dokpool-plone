import Base from "@patternslib/patternslib/src/core/base";
import logger from "@patternslib/patternslib/src/core/logging";
import registry from "@patternslib/patternslib/src/core/registry";
import parseBodyTag from "./utils";
import _ from "underscore";

const log = logger.getLogger("pat-contentloader-bfs");

export default Base.extend({
  name: "contentloader-bfs",
  trigger: ".pat-contentloader-bfs",
  parser: "mockup",
  defaults: {
    url: null,
    content: null,
    trigger: "click",
    target: null,
    template: null,
    dataType: "html",
  },
  init: function () {
    var that = this;
    if (that.options.url === "el" && that.$el[0].tagName === "A") {
      that.options.url = that.$el.attr("href");
    }
    that.$el.removeClass("loading-content");
    that.$el.removeClass("content-load-error");
    if (that.options.trigger === "immediate") {
      that._load();
    } else {
      that.$el.on(that.options.trigger, function (e) {
        e.preventDefault();
        that._load();
      });
    }
  },
  _load: function () {
    var that = this;
    that.$el.addClass("loading-content");
    that.$el.toggleClass("close");
    // State :)
    var $metadata = false;
    var $metatitle = false;
    // Is the other meta column open? If close it
    let other_column = that.$el.parent().find("a").not(".loading-content");
    if (other_column != that.$el) {
      if (other_column.hasClass("close")) {
        other_column.removeClass("close");
      }
    }
    var $already_open = that.$el.closest("tr").next("tr");
    if ($already_open.hasClass("target_open")) {
      $already_open.remove();
    } else {
      if (that.options.url) {
        // Load Metadata
        that.loadRemote();
      } else {
        // Load Metatitle
        that.loadLocal();
      }
    }
  },
  loadRemote: function () {
    var that = this;
    $.ajax({
      url: that.options.url,
      dataType: that.options.dataType,
      success: function (data) {
        var $el;
        if (that.options.dataType === "html") {
          if (data.indexOf("<html") !== -1) {
            data = parseBodyTag(data);
          }
          $el = $('<tr class="target_open"><td>&nbsp</td><td>&nbsp</td> <td>&nbsp</td><td colspan="3">' + data + "</td> <td>&nbsp</td> <td>&nbsp</td></tr>"); // jQuery starts to search at the first child element.
        } else if (that.options.dataType.indexOf("json") !== -1) {
          // must have template defined with json
          if (data.constructor === Array && data.length === 1) {
            // normalize json if it makes sense since some json returns as array with one item
            data = data[0];
          }
          try {
            $el = $(_.template(that.options.template)(data));
          } catch (e) {
            that.$el.removeClass("loading-content");
            that.$el.addClass("content-load-error");
            log.warn("error rendering template. pat-contentloader will not work");
            return;
          }
        }
        if (that.options.content !== null) {
          $el = $el.find(that.options.content);
        }
        that.loadLocal($el);
      },
      error: function () {
        that.$el.removeClass("loading-content");
        that.$el.addClass("content-load-error");
      },
    });
  },
  loadLocal: function ($content) {
    var that = this;
    if (!$content && that.options.content === null) {
      that.$el.removeClass("loading-content");
      that.$el.addClass("content-load-error");
      log.warn("No selector configured");
      return;
    }
    var $target = that.$el;
    if (that.options.target !== null) {
      $target = $(that.options.target);
      if ($target.length === 0) {
        that.$el.removeClass("loading-content");
        that.$el.addClass("content-load-error");
        log.warn("No target nodes found");
        return;
      }
    }

    if (!$content) {
      var $content_raw = $(that.options.content).clone();
      $content = $('<tr class="target_open"><td>&nbsp</td><td>&nbsp</td> <td>&nbsp</td><td colspan="3"><h4>' + $content_raw.text() + "</h4></td> <td>&nbsp</td> <td>&nbsp</td></tr>"); // jQuery starts to search at the first child element.
    }
    $target = $target.closest("tr");
    if ($content.length) {
      $content.show();
      $target.after($content);
      registry.scan($content);
    } else {
      // empty target node instead of removing it.
      // allows for subsequent content loader calls to work sucessfully.
      $target.empty();
    }

    that.$el.removeClass("loading-content");
    that.emit("loading-done");
  },
});

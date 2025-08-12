import registry from "@patternslib/patternslib/src/core/registry";
import "./src/update-notification";

// Import styles directly in the JavaScript pattern.
// Webpack will automatically create a CSS file for it and inject it into the
// page on top of the HEAD element.
window.__patternslib_import_styles = true;

registry.init();

// Webpack entry point for module federation.

// This import needs to be kept with brackets, otherwise we get this error:
// "Shared module is not available for eager consumption."
import("./bundle");

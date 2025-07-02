process.traceDeprecation = true;
const mf_config = require("@patternslib/dev/webpack/webpack.mf");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const package_json = require("./package.json");
const package_json_mockup = require("@plone/mockup/package.json");
const package_json_patternslib = require("@patternslib/patternslib/package.json");
const path = require("path");
const webpack_config = require("@patternslib/dev/webpack/webpack.config").config;

module.exports = () => {
  let config = {
    entry: {
      "docpool.ui.min": path.resolve(__dirname, "./src/docpool.ui/docpool/ui/resources/index.js"),
      barceloneta: path.resolve(__dirname, "./src/docpool.ui/docpool/ui/resources/barceloneta/barceloneta.scss"),
      docpool: path.resolve(__dirname, "./src/docpool.ui/docpool/ui/resources/docpool.scss"),
    },
  };

  config = webpack_config({
    config: config,
    package_json: package_json,
  });
  config.output.path = path.resolve(__dirname, "src/docpool.ui/docpool/ui/static/build");

  config.plugins.push(
    mf_config({
      name: "docpool.ui",
      filename: "docpool.ui-remote.min.js",
      remote_entry: config.entry["docpool.ui.min"],
      dependencies: {
        ...package_json_patternslib.dependencies,
        ...package_json_mockup.dependencies,
        ...package_json.dependencies,
      },
    }),
  );

  // Compile our docpool styling and bootstrap separate from the other files,
  // to be loaded immediately to avoid flash of unstyled content.
  config.plugins.push(new MiniCssExtractPlugin());
  config.module.rules.push({
    test: /docpool\.scss$/,
    use: [MiniCssExtractPlugin.loader, "css-loader", "postcss-loader", "sass-loader"],
  });
  config.module.rules.push({
    test: /barceloneta\.scss$/,
    use: [MiniCssExtractPlugin.loader, "css-loader", "postcss-loader", "sass-loader"],
  });
  if (process.env.NODE_ENV === "development") {
    config.devServer.port = "3001";
    config.devServer.static.directory = path.resolve(__dirname, "./src/docpool.ui/docpool/ui/resources/index.js");
  }

  // Debug output
  //console.log(JSON.stringify(config, null, 4));

  return config;
};

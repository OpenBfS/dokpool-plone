process.traceDeprecation = true;
const mf_config = require("@patternslib/dev/webpack/webpack.mf");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const package_json = require("./package.json");
const package_json_mockup = require("@plone/mockup/package.json");
const package_json_patternslib = require("@patternslib/patternslib/package.json");
const path = require("path");
const webpack_config =
  require("@patternslib/dev/webpack/webpack.config").config;

module.exports = () => {
  let config = {
    entry: {
      "docpool.theme.min": path.resolve(
        __dirname,
        "./src/docpool.theme/docpool/theme/resources/index.js",
      ),
      "elan.journal.min": path.resolve(
        __dirname,
        "./src/elan.journal/elan/journal/resources/index.js",
      ),
      "docpool.config.min": path.resolve(
        __dirname,
        "./src/docpool.config/docpool/config/resources/index.js",
      ),
      "docpool.base.min": path.resolve(
        __dirname,
        "./src/docpool.base/docpool/base/resources/index.js",
      ),
      "docpool.elan.min": path.resolve(
        __dirname,
        "./src/docpool.elan/docpool/elan/resources/index.js",
      ),
      "docpool.rei.min": path.resolve(
        __dirname,
        "./src/docpool.rei/docpool/rei/resources/index.js",
      ),
      barceloneta: path.resolve(
        __dirname,
        "./src/docpool.theme/docpool/theme/resources/barceloneta.scss",
      ),
    },
  };

  config = webpack_config({
    config: config,
    package_json: package_json,
  });
  config.output.path = path.resolve(
    __dirname,
    "src/docpool.theme/docpool/theme/static/build",
  );

  config.plugins.push(
    mf_config({
      name: "docpool.theme",
      filename: "docpool.theme-remote.min.js",
      remote_entry: config.entry["docpool.theme.min"],
      dependencies: {
        ...package_json_patternslib.dependencies,
        ...package_json_mockup.dependencies,
        ...package_json.dependencies,
      },
    }),
  );

  config.plugins.push(
    mf_config({
      name: "elan.journal.min",
      filename: "elan.journal-remote.min.js",
      remote_entry: config.entry["elan.journal.min"],
      dependencies: {
        ...package_json_patternslib.dependencies,
        ...package_json_mockup.dependencies,
        ...package_json.dependencies,
      },
    }),
  );

  config.plugins.push(
    mf_config({
      name: "docpool.config",
      filename: "docpool.config-remote.min.js",
      remote_entry: config.entry["docpool.config.min"],
      dependencies: {
        ...package_json_patternslib.dependencies,
        ...package_json_mockup.dependencies,
        ...package_json.dependencies,
      },
    }),
  );

  config.plugins.push(
    mf_config({
      name: "docpool.base",
      filename: "docpool.base-remote.min.js",
      remote_entry: config.entry["docpool.base.min"],
      dependencies: {
        ...package_json_patternslib.dependencies,
        ...package_json_mockup.dependencies,
        ...package_json.dependencies,
      },
    }),
  );

  config.plugins.push(
    mf_config({
      name: "docpool.elan",
      filename: "docpool.elan-remote.min.js",
      remote_entry: config.entry["docpool.elan.min"],
      dependencies: {
        ...package_json_patternslib.dependencies,
        ...package_json_mockup.dependencies,
        ...package_json.dependencies,
      },
    }),
  );

  config.plugins.push(
    mf_config({
      name: "docpool.rei",
      filename: "docpool.rei-remote.min.js",
      remote_entry: config.entry["docpool.rei.min"],
      dependencies: {
        ...package_json_patternslib.dependencies,
        ...package_json_mockup.dependencies,
        ...package_json.dependencies,
      },
    }),
  );

  // Compile our base barceloneta separate from the other files
  config.plugins.push(new MiniCssExtractPlugin());
  config.module.rules.push({
    test: /barceloneta\.scss$/,
    use: [
      MiniCssExtractPlugin.loader,
      "css-loader",
      "postcss-loader",
      "sass-loader",
    ],
  });
  if (process.env.NODE_ENV === "development") {
    config.devServer.port = "3001";
    config.devServer.static.directory = path.resolve(__dirname, "./resources/");
  }

  // Debug output
  //console.log(JSON.stringify(config, null, 4));

  return config;
};

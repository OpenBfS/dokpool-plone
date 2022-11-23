process.traceDeprecation = true;
const path = require("path");

module.exports = [
    {
        // Main bundle
        entry: ["./src/docpool.theme/docpool/theme/resources/default.js",
            "./src/elan.journal/elan/journal/resources/default.js",
            "./src/docpool.elan/docpool/elan/resources/default.js",
            "./src/docpool.rei/docpool/rei/resources/default.js"],
        // Disable for debugging and development
        optimization: {
            minimize: true,
        },
        output: {
            path: path.resolve(__dirname, "src/docpool.theme/docpool/theme/static/"),
            filename: "docpool.min.js",
        },
        module: {
            rules: [
                {
                    test: /\.s[ac]ss$/i,
                    use: [
                        // Creates `style` nodes from JS strings
                        {loader: "style-loader"},
                        // Translates CSS into CommonJS
                        {
                            loader: "css-loader",
                            options: {
                                url: false,
                            },
                        },
                        // Compiles Sass to CSS
                        {loader: "sass-loader"},
                    ],
                },
            ],
        },
    },
];

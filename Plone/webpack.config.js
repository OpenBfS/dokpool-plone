process.traceDeprecation = true;
const path = require("path");

module.exports = [
    {
        // Main bundle
        entry: './src/docpool.theme/docpool/theme/resources/docpool.js',
        //optimization: {
        //     minimize: true,
        //},
        output: {
            path: path.resolve(__dirname, 'src/docpool.theme/docpool/theme/static/'),
            filename: 'docpool.min.js',
        },
    },
];
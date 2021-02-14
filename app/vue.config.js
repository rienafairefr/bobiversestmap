const CopyPlugin = require("copy-webpack-plugin");
const path = require("path");

module.exports = {
    configureWebpack: {
        plugins: [
            new CopyPlugin({
                patterns: [
                    {
                        from: path.resolve(__dirname, "../docs"),
                        to: "data",
                    },
                ]
            }),
        ]
    }
}
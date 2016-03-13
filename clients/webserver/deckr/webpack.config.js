var path = require("path")
var webpack = require("webpack")
var BundleTracker = require("webpack-bundle-tracker")

module.exports = {
	context: __dirname,
	entry: "./webclient/static/js/game/index",
	output: {
		path: path.resolve("./webclient/static/bundles/"),
		filename: "[name]-[hash].js"
	},
	plugins: [
		new BundleTracker({filename: "./webpack-stats.json"})
	],
	module: {
		loaders: [
			{test: /\.jsx?$/, exclude: /node_modules/, loader: "babel-loader"}
		]
	},
	resolve: {
		modulesDirectories: ["node_modules", "bower_components"],
		extensions: ["", ".js", ".jsx"]
	},
}

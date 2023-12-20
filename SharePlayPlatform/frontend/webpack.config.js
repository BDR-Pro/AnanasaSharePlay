const path = require("path");
const webpack = require("webpack");

module.exports = {
  devtool: 'eval-source-map',
  entry: {
    signUp:"./src/components/comp_signUp.js"  // Update the path to your detail.js
  },
  // webpack.config.js
resolve: {
  extensions: ['.js', '.json', '.wasm'],
},

  output: {
    path: path.resolve(__dirname, "./static/frontend"),
    filename: "[name].js",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  optimization: {
    minimize: true,
  },
  plugins: [
    new webpack.DefinePlugin({
      "process.env": {
        NODE_ENV: JSON.stringify("production"),
      },
    }),
  ],
};

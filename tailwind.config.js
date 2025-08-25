const path = require('path');

module.exports = {
  content: [
    path.join(__dirname, 'templates/**/*.html'),
    path.join(__dirname, 'trades/templates/**/*.html'),
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};

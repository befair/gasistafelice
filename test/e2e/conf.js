// conf.js
exports.config = {
  seleniumAddress: 'http://hub:4444/wd/hub',
  specs: ['spec.js'],
  multiCapabilities: [
    { browserName: "firefox" },
    { browserName: "chrome" }
  ]
}

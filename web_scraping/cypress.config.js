const uas = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0'
]

function pickUA() {
  const i = Math.floor(Math.random() * uas.length)
  return uas[i]
}

module.exports = {
  e2e: {
    specPattern: 'cypress/e2e/**/*.cy.{js,ts}',
    supportFile: 'cypress/support/e2e.js',
    chromeWebSecurity: false,
    defaultCommandTimeout: 20000,
    pageLoadTimeout: 90000,
    requestTimeout: 30000,
    responseTimeout: 30000,
    experimentalModifyObstructiveThirdPartyCode: true,
    watchForFileChanges: false,
    video: false,
    screenshotOnRunFailure: true,
    env: {
      URL: 'https://shopee.co.th/',
      OUT: 'shopee_thailand_cypress.html'
    },
    setupNodeEvents(on, config) {
      // Handle file operations and other node events
      on('task', {
        log(message) {
          console.log(message)
          return null
        }
      })
    }
  },
  userAgent: pickUA(),
}


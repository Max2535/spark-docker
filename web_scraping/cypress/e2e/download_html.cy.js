/// <reference types="cypress" />

function humanScroll(times = 3) {
  for (let i = 0; i < times; i++) {
    cy.wait(600 + Math.floor(Math.random() * 700))
    cy.scrollTo('bottom', { ensureScrollable: false })
  }
}

describe('Download rendered HTML', () => {
  it('visits target and saves HTML', () => {
    const url = Cypress.env('URL') || 'https://shopee.co.th/'
    const out = Cypress.env('OUT') || 'web_scraping/shopee_thailand_cypress.html'

    const viewports = [
      [1366, 768],
      [1536, 864],
      [1920, 1080],
    ]
    const [w, h] = viewports[Math.floor(Math.random() * viewports.length)]
    cy.viewport(w, h)

    // Visit the URL with enhanced error handling
    cy.visit(url, {
      timeout: 90000,
      failOnStatusCode: false,
      onBeforeLoad(win) {
        // Reduce obvious automation fingerprints
        Object.defineProperty(win.navigator, 'webdriver', { get: () => undefined })
        Object.defineProperty(win.navigator, 'languages', { get: () => ['th-TH', 'th', 'en-US', 'en'] })
        Object.defineProperty(win.navigator, 'plugins', { get: () => [1, 2, 3] })
        win.chrome = win.chrome || { runtime: {} }
        
        // Add more realistic navigator properties
        Object.defineProperty(win.navigator, 'hardwareConcurrency', { get: () => 4 })
        Object.defineProperty(win.navigator, 'deviceMemory', { get: () => 8 })
        Object.defineProperty(win.navigator, 'platform', { get: () => 'MacIntel' })
      },
    })

    // Wait for initial page load
    cy.wait(3000)
    
    // Handle consent popups using custom command
    cy.handleConsent()

    // Wait for page stability
    cy.waitForPageStability()
    
    // Perform human-like scrolling
    humanScroll(4)

    // Wait for final content to load
    cy.wait(2000)
    
    // Get the final HTML and save it
    cy.document().then((doc) => {
      const html = '<!DOCTYPE html>\n' + doc.documentElement.outerHTML
      cy.writeFile(out, html, 'utf8')
      cy.log(`HTML saved to: ${out}`)
    })
  })
})


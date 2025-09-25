// Custom Cypress commands

// Add command to safely click elements
Cypress.Commands.add('safeClick', (selector, options = {}) => {
  cy.get('body').then(($body) => {
    if ($body.find(selector).length > 0) {
      cy.get(selector).first().click({ force: true, ...options })
    }
  })
})

// Add command to wait for page stability
Cypress.Commands.add('waitForPageStability', (timeout = 5000) => {
  let previousHeight = 0
  let stableCount = 0
  const checkStability = () => {
    cy.document().then((doc) => {
      const currentHeight = doc.body.scrollHeight
      if (currentHeight === previousHeight) {
        stableCount++
      } else {
        stableCount = 0
        previousHeight = currentHeight
      }
      
      if (stableCount < 3) {
        cy.wait(500).then(checkStability)
      }
    })
  }
  
  checkStability()
})

// Add command to handle consent popups more gracefully
Cypress.Commands.add('handleConsent', () => {
  const consentSelectors = [
    'button:contains("ยอมรับ")',
    'button:contains("ตกลง")',
    'button:contains("Accept")',
    'button:contains("OK")',
    'button:contains("ปิด")',
    '[data-testid*="accept"]',
    '[data-testid*="consent"]',
    '.consent-accept',
    '.accept-cookies',
    '.gdpr-accept'
  ]
  
  consentSelectors.forEach(selector => {
    cy.get('body').then(($body) => {
      if ($body.find(selector).length > 0) {
        cy.get(selector).first().click({ force: true })
        cy.wait(500) // Wait a bit after clicking
      }
    })
  })
})
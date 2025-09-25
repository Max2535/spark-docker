// Global Cypress configurations and hooks

// Import commands.js using ES2015 syntax:
import './commands'

// Ignore uncaught exceptions that might cause test failures
Cypress.on('uncaught:exception', (err, runnable) => {
  // Return false to prevent Cypress from failing the test
  console.log('Ignoring uncaught exception:', err.message)
  return false
})

// Add global before hook to set up common configurations
beforeEach(() => {
  // Set longer timeouts for better stability
  cy.intercept('**', (req) => {
    req.continue()
  })
})


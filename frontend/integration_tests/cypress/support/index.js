// ***********************************************************
// This example support/index.js is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import './commands'

before(() => {
    localStorage.clear();
    localStorage.setItem('AUTH-TOKEN', 'cytesttoken');
    cy.intercept('**/auth/user', { body: {
        'id': 4,
        'username': 'testuser',
        'email': 'testemail@testuser.com',
    } });
    cy.visit('/');
})

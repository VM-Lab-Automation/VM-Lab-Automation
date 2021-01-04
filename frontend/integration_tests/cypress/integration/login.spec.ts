
/// <reference types="cypress" />

context('Login', () => {

  beforeEach(() => {
      cy.get('.login-button') // logout at this moment
        .click()
      cy.visit('/login')
  });
  
  it('should login', () => {
      cy.get('#user-group-username')
        .type('cyuser');
      cy.get('#user-group-password')
        .type('cypass');
      
      cy.intercept('**/api/auth/login', {
        body: {
          token: 'testtoken'
        }
      }).as('loginRequest');
      cy.intercept('**/api/labs', {
        body: []
      });

      cy.get('.login-form button')
        .click();

      cy.wait('@loginRequest').should(r => {
        expect(r.request.body.username).to.equal('cyuser');
        expect(r.request.body.password).to.equal('cypass');
      });
  })
})
  
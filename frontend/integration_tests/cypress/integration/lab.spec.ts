/// <reference types="cypress" />

context('Labs', () => {
  const labs = [{
    'id': '34ifm32jkdf',
    'name': 'First mock lab',
    'worker_id': 'first_worker',
    'created_date': '2020-04-01',
    'lab_type': 'Kathara',
    'start_date': '2020-06-06',
    'expiration_date': '2020-06-07',
    'description': 'mocked description',
    'vm_count': 2,
    'status': 'RUNNING'
  },{
    'id': '7984jdhf832hd',
    'name': 'Second mock lab',
    'worker_id': 'first_worker',
    'created_date': '2020-05-01',
    'lab_type': 'Basic',
    'start_date': '2020-05-06',
    'expiration_date': '2020-05-07',
    'description': 'Mocked description',
    'vm_count': 2,
    'status': 'EXPIRED'
  }];

  beforeEach(() => {
    cy.intercept('**/api/labs', {
        body: labs
    })
    cy.visit('/labs');
  });

  it('should display labs for user and open details', () => {
    cy.intercept('**/api/labs/34if*', {
      body: {
        'id': '34ifm32jkdf',
        'name': 'First mock lab',
        'worker_id': 'first_worker',
        'created_date': '2020-04-01',
        'lab_type': 'Kathara',
        'start_date': '2020-06-06',
        'expiration_date': '2020-06-07',
        'description': 'mocked description',
        'vm_count': 2,
        'status': 'RUNNING',
        'machines': [
          { 
            id: 'node-1',
            name: 'kowalski',
            status: 'stopped',
            rdp_address: '1.2.3.4:5',
            ssh_address: '1.2.3.4:6',
            login: 'root',
            password: 'no access' 
          },
          { 
            id: 'node-2',
            name: 'nowak',
            status: 'running',
            rdp_address: '1.2.3.4:7',
            ssh_address: '1.2.3.4:8',
            login: 'root',
            password: 'accessgranted' 
          }
        ]
      }
    })
    cy.get('.lab-card .lab-config-button').first().click();
  });
})
  
import React, { Component, useEffect, useState } from 'react';
import LabList from './components/labs/LabsList';
import { HashRouter as Router, Route, Switch, Redirect, useHistory } from 'react-router-dom'
import WorkersList from './components/workers/WorkersList';
import { Button, Nav, Navbar, NavDropdown } from 'react-bootstrap';
import LabForm from './components/labs/LabForm';
import LoginComponent from './components/login/Login';
import { AuthService } from './services/AuthService';
import { LabService } from './services/LabService';
import { WorkerService } from './services/WorkerService';


const App: React.FunctionComponent = () => {
  const authService = new AuthService();
  
  const [ isAuthenticated, setIsAuthenticated ] = useState<boolean>(authService.isLoggedIn());
  const [ currentUserName, setCurrentUserName ] = useState<string>('');
  
  useEffect(() => {
    const displayCurrentUserName = async () => {
      const name = await authService.getUserName();
      if(name) {
        setCurrentUserName(name);
      }
    }
    displayCurrentUserName();
  }, [ isAuthenticated, authService ]);
  
  
  const logout = () => {
    authService.logout();  
    setIsAuthenticated(false);
  }

  type AppRoute = {Component: any, path: string}

  const GuardedRoute: (p: AppRoute) => any = ({ Component, path, ...rest }) => (
    <Route exact path={path} render={(props) => (
        isAuthenticated
            ? <Component {...props} {...rest} />
            : <Redirect to='/login' />
    )} />) 
  

  return (
    <Router>
      <div>
        <Navbar bg="dark" variant="dark">
          <Nav className="mr-auto">
            <NavDropdown id="labs" title="Labs">
              <NavDropdown.Item href="#labs">List all labs</NavDropdown.Item>
              <NavDropdown.Item href="#lab-form">Create a new one</NavDropdown.Item>
            </NavDropdown>
            <Nav.Link href="#workers">Workers</Nav.Link>
          </Nav>
          { !isAuthenticated 
            ? (<Button href="#login" className="login-button">Login</Button>) 
            : (<div>
                { currentUserName && <span className="logged-as-prompt">Logged as: {currentUserName} </span> }
                <Button href="#login" onClick={() => logout()} className="login-button">Logout</Button>
              </div>)}
        </Navbar>
        <Switch>
          <Redirect exact from="/" to="/labs" />
          <Route exact path="/login" render={(props) => <LoginComponent {...props} onAuthenticated={() => setIsAuthenticated(true)}></LoginComponent>}></Route>
          <GuardedRoute path="/labs" Component={LabList}></GuardedRoute>
          <GuardedRoute path="/lab-form" Component={LabForm}></GuardedRoute>
          <GuardedRoute path="/workers" Component={WorkersList}></GuardedRoute>
        </Switch>
      </div>
    </Router>
  );
}

export default App;

import React, { FormEvent, useState } from 'react';
import {Alert, Button, Form} from 'react-bootstrap';
import { useHistory } from 'react-router-dom';
import { AuthService } from '../../services/AuthService';

interface Props {
    onAuthenticated: () => void;
}

const LoginComponent: React.FunctionComponent<any> = ({ onAuthenticated }: Props) => {
    
    const history = useHistory();
    const [error, setError] = useState<string>();
    
    const loginHandler = async (event: FormEvent<HTMLFormElement>) => {
        setError('');
        event.preventDefault();

        const form = event.currentTarget as HTMLFormElement;
        const nameInput = form.elements.namedItem('username') as HTMLInputElement;
        const typeInput = form.elements.namedItem('password') as HTMLSelectElement;
   
        try {
            const authService = new AuthService();
            await authService.login(nameInput.value, typeInput.value);
            onAuthenticated();
            history.replace('/labs');
        } catch(e) {
            console.log(e);
            setError(e.message);
        }
    }

    return (
        <div className="login-form">
            { error && <Alert key='error-message' variant='danger'>
                {error}
            </Alert> }
            <Form onSubmit={loginHandler}>
                <Form.Group controlId="user-group-username">
                    <Form.Label>Username</Form.Label>
                    <Form.Control type="text" name="username" placeholder="Enter username"/>
                </Form.Group>
                <Form.Group controlId="user-group-password">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" name="password" placeholder="Enter password"/>
                </Form.Group>
                <Button variant="primary" type="submit">Login</Button>
            </Form>
        </div>
    );
}

export default LoginComponent;
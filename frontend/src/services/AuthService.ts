import apiPaths from "./APIPaths";
import { getAuthToken, getDefaultAuthHeader, setAuthToken } from "./AuthToken";
import { throwExceptionWhenFailed } from "./APIUtils";

export class AuthService{

    async login(username: string, password: string){
        const requestBody = JSON.stringify({
            username,
            password
        });

        const response = await fetch(apiPaths.login, {
            method: 'post',
            body: requestBody,
            headers: {
                'Content-Type': 'application/json'
            }
        });

        await throwExceptionWhenFailed(response);
        const responseBody = await response.json();
        setAuthToken(responseBody['token']);
    }

    async getUserName() {
        if(!this.isLoggedIn()) {
            return null;
        }

        const response = await fetch(apiPaths.user, {
            method: 'get',
            headers: {
                'Content-Type': 'application/json',
                ...getDefaultAuthHeader()
            }
        });

        const user = await response.json(); 

        return user.username;
    }

    logout() {
        setAuthToken('');
    }

    isLoggedIn() {
        return !!getAuthToken(); 
    }
}
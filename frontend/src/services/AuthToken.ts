
export const getAuthToken = () => {
    return localStorage.getItem('AUTH-TOKEN');
}

export const setAuthToken = (token: string) => {
    return localStorage.setItem('AUTH-TOKEN', token);
}

export const getDefaultAuthHeader = () => {
    return {
        'Authorization': 'Bearer ' + getAuthToken()
    }
}
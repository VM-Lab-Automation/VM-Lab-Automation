export class ApiException {
    constructor(public status: number, public message: string) {}
}

export const throwExceptionWhenFailed = async (response: Response) => {
    if(!response.ok) {
        throw new ApiException(response.status, (await response.json()).message)
    }
}
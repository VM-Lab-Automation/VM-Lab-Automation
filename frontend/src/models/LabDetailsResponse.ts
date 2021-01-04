export interface LabDetailsResponse{
    lab_id: string,
    lab_name: string,
    status: string,
    start_date: string,
    expiration_date: string,
    machines: [{
        id: string,
        name: string,
        status: string,
        rdp_address: string,
        ssh_address: string,
        login: string,
        password: string
    }]
}
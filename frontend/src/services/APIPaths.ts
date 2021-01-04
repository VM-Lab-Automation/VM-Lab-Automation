const apiPrefix = '/api'
const apiPaths = {
    labs: `${apiPrefix}/labs`,
    workers: `${apiPrefix}/workers`,
    labTypes: `${apiPrefix}/lab-types`,
    lab: (labId: string) => `${apiPrefix}/labs/${labId}`,
    machineStart: (labId: string, vmId: string) => `${apiPrefix}/labs/${labId}/machine/${vmId}/start`,
    labFiles: (labId: string) => `${apiPrefix}/labs/${labId}/machine_files`,
    login: `${apiPrefix}/auth/login`,
    user: `${apiPrefix}/auth/user`
}

export default apiPaths
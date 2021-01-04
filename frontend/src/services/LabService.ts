import { LabRequest } from "../models/LabRequest";
import { LabResponse } from "../models/LabResponse";
import apiPaths from "./APIPaths";
import {LabDetailsResponse} from "../models/LabDetailsResponse";
import { getDefaultAuthHeader } from "./AuthToken";
import { throwExceptionWhenFailed } from "./APIUtils";

export class LabService{

    async getAllLabs(){
        const response = await fetch(apiPaths.labs, {
            method: 'get',
            headers: { ...getDefaultAuthHeader() }
        }); 
        await throwExceptionWhenFailed(response);
        return await response.json() as LabResponse[]; 
    }

    async createLab(request: LabRequest){
        const requestBody = JSON.stringify(request);

        await fetch(apiPaths.labs, {
            method: 'post',
            body: requestBody,
            headers: {
                'Content-Type': 'application/json',
                ...getDefaultAuthHeader()
            }
        })
    }

    async getLabTypes(): Promise<string[]>{
        const response = await fetch(apiPaths.labTypes, {
            method: 'get'
        });
        return await response.json();
    }

    async getLabDetails(lab_id: string): Promise<LabDetailsResponse> {
        const response = await fetch(apiPaths.lab(lab_id), {
            method: 'get',
            headers: { ...getDefaultAuthHeader() }
        });
        return await response.json() as LabDetailsResponse;
    }

    async restartMachine(lab_id: string, vm_id: string) {
        fetch(apiPaths.machineStart(lab_id, vm_id), {
            method: 'put',
            headers: { ...getDefaultAuthHeader() }
        });
    }
}
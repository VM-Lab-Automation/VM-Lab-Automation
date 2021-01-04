import { WorkerResponse } from "../models/WorkerResponse";
import apiPaths from "./APIPaths";

export class WorkerService{

    async getAllWorkers(){

        const response = await fetch(apiPaths.workers, {
            method: 'get'
        }); 
        return await response.json() as WorkerResponse[]; 
    }
}
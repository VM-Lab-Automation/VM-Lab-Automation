import React, { useState } from 'react';
import { useEffect } from 'react';
import {Badge, Card, Spinner} from 'react-bootstrap';
import { WorkerResponse } from '../../models/WorkerResponse';
import formatDate from '../../utils/DateFormatter';
import { WorkerService } from '../../services/WorkerService';

const WorkersList: React.FunctionComponent = () => {
    const workerService = new WorkerService();
    
    const [workers, setWorkers] = useState<WorkerResponse[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const getWorkers = async () => {
            const l = await workerService.getAllWorkers();
            setWorkers(l);
            setIsLoading(false);
        }
        getWorkers();
    }, [])

    const getBadge = (state: number) => {
        return state === 1 ? 
            <Badge pill variant="success">Running</Badge> 
            : <Badge pill variant="danger">Not running</Badge>
    }

    return(
        <div className="worker-list">
            <h3>Workers</h3>
            {isLoading ?
                <Spinner className="custom-spinner" animation="border"/> :

                workers.map(worker => (
                <Card key={worker.worker_id} className="worker-card">
                    <Card.Header>
                        <b>{worker.worker_id}</b> {getBadge(worker.state)}
                        </Card.Header>
                    <Card.Body>
                        <Card.Text><b>Host:</b> {worker.host}</Card.Text>
                        <Card.Text><b>Api port:</b> {worker.api_port}</Card.Text>
                        <Card.Text><b>Last update:</b> {formatDate(worker.last_update)}</Card.Text>
                    </Card.Body>
                </Card>
            ))}
        </div>
    );
}

export default WorkersList;
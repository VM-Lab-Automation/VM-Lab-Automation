import React, { useState } from 'react'
import { useEffect } from 'react';
import {Card, Button, Badge, Spinner} from 'react-bootstrap';
import { LabResponse } from '../../models/LabResponse';
import formatDate from '../../utils/DateFormatter';
import { LabService } from '../../services/LabService';
import LabModal from "./LabModal";
import LabFilesButton from "./LabFilesButton";


const LabList: React.FunctionComponent = () => {
    const labService = new LabService();

    const [labs, setLabs] = useState<LabResponse[]>([]);
    const [error, setError] = useState<string>();
    const [isLoading, setIsLoading] = useState(true);

    const [selectedLabId, setSelectedLabId] = useState('');
    const [show, setShow] = useState(false);

    useEffect(() => {
        const getLabs = async () => {
            try {
                const l = await labService.getAllLabs();
                setLabs(l);
                setIsLoading(false);
            } catch(e) {
                setError(e.message);
            }
        };
        getLabs();
    }, []);

    const handleShow = (lab_id: string) => {
        setSelectedLabId(lab_id);
        setShow(true);
    }

    const handleClose = () => setShow(false);

    const getBadge = (status: string) => {
        switch(status) {
            case "PREPARING":
                return <Badge pill variant="info">Preparing</Badge>
            case "SETTING_UP":
                return <Badge pill variant="primary">Setting up</Badge>
            case "SETUP_ERROR":
                return <Badge pill variant="danger">Setup error</Badge>
            case "RUNNING":
                return <Badge pill variant="success">Running</Badge>
            case "PARTIALLY_RUNNING":
                return <Badge pill variant="warning">Partially running</Badge>
            case "NOT_RUNNING":
                return <Badge pill variant="danger">Not running</Badge>
            case "EXPIRED":
                return <Badge pill variant="secondary">Expired</Badge>
            default:
                return <Badge pill variant="dark">Status unknown</Badge>
        }
    }

    return (
        <div className="lab-list">
            {show && <LabModal lab_id={selectedLabId} close={handleClose}/>}

            <h3>Labs</h3>
            {isLoading ?
                <Spinner className="custom-spinner" animation="border"/> :

                labs && labs.map(lab => (
                    <Card key={lab.id} className="lab-card">
                        <Card.Header>{lab.name} {getBadge(lab.status)}</Card.Header>
                        <Card.Body>
                            <div className="row">
                                <div className="col">
                                    <Card.Text><b>Id:</b> {lab.id}</Card.Text>
                                    <Card.Text><b>Created date:</b> {formatDate(lab.created_date)}</Card.Text>
                                    <Card.Text><b>Worker id:</b> {lab.worker_id}</Card.Text>
                                    <Card.Text><b>Lab type:</b> {lab.lab_type}</Card.Text>
                                </div>
                                <div className="col">
                                    <Card.Text><b>Start date:</b> {formatDate(lab.start_date)}</Card.Text>
                                    <Card.Text><b>Expiration date:</b> {formatDate(lab.expiration_date)}</Card.Text>
                                    <Card.Text><b>Description:</b> {lab.description}</Card.Text>
                                    <Card.Text><b>Virtual machines count:</b> {lab.vm_count}</Card.Text>
                                    <Button className="lab-config-button" variant="primary" onClick={() => handleShow(lab.id)}>Show config</Button>
                                    <LabFilesButton lab_id={lab.id}/>
                                </div>
                            </div>
                        </Card.Body>
                    </Card>
                ))}
        </div>
    );
}

export default LabList;
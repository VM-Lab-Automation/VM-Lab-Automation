import React, { useState } from 'react'
import { useEffect } from 'react';
import {Button, Modal, Badge, Table, Spinner} from 'react-bootstrap';
import { LabService } from '../../services/LabService';
import {LabDetailsResponse} from "../../models/LabDetailsResponse";
import RestartButton from "./RestartButton";


interface Props {
  lab_id: string;
  close: () => void;
}

const LabModal: React.FunctionComponent<Props> = ({
    lab_id,
    close
  }: Props) => {

    const [labDetails, setLabDetails] = useState<LabDetailsResponse>();
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const labService = new LabService();
        const getLabDetails = async (id: string) => {
            const labDetails = await labService.getLabDetails(id);
            setLabDetails(labDetails);
            setIsLoading(false);
        };
        getLabDetails(lab_id);
    }, [lab_id])

    const getVMBadge = (status: string) => {
        switch(status.toLowerCase()) {
            case "running":
                return <Badge pill variant="success">Running</Badge>
            case "stopped":
                return <Badge pill variant="danger">Not running</Badge>
            default:
                return <Badge pill variant="dark">Status unknown</Badge>
        }
    }
    return (
        <div>
            <Modal show={true} size="xl">
                <Modal.Header>
                    <Modal.Title><b>Lab name:</b> {labDetails?.lab_name}</Modal.Title>
                </Modal.Header>

                {isLoading ?
                    <Spinner className="custom-spinner" animation="border"/> :

                    <Modal.Body>
                        Virtual machines
                        <Table>
                            <tbody>
                                <tr>
                                    <th>Name</th>
                                    <th>RDP</th>
                                    <th>SSH</th>
                                    <th>Login</th>
                                    <th>Password</th>
                                    <th></th>
                                </tr>
                                {labDetails?.machines.map(machine => (
                                    <tr key={machine.name}>
                                        <td>{machine.name} {getVMBadge(machine.status)}</td>
                                        <td>{machine.rdp_address}</td>
                                        <td>{machine.ssh_address}</td>
                                        <td>{machine.login}</td>
                                        <td>{machine.password}</td>
                                        <td><RestartButton lab_id={lab_id}
                                                           vm_id={machine.id}
                                                           vm_status={machine.status}
                                                           expiration_date={labDetails?.expiration_date}/></td>
                                    </tr>
                                ))}
                            </tbody>
                        </Table>
                    </Modal.Body>
                }

                <Modal.Footer>
                    <Button variant="secondary" onClick={close}>Close</Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
}

export default LabModal;
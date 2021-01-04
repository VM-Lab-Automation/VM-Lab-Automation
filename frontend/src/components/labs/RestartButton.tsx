import React, {useState} from 'react'
import {Button} from "react-bootstrap";
import {LabService} from "../../services/LabService";

interface Props {
  lab_id: string;
  vm_id: string;
  vm_status: string;
  expiration_date: string;
}

const RestartButton: React.FunctionComponent<Props> = ({
    lab_id,
    vm_id,
    vm_status,
    expiration_date
    }: Props) => {

    const [disable, setDisable] = useState(vm_status.toLowerCase() === "running" || Date.parse(expiration_date) < Date.now())

    const start_vm = () => {
        setDisable(true)
        const labService = new LabService();
        labService.restartMachine(lab_id, vm_id)
    }

    return (
        <Button variant="primary" onClick={start_vm} disabled={disable}>
            Restart
        </Button>
    );
}

export default RestartButton;
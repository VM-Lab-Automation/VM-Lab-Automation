import React, {useEffect, useState} from 'react';
import { FormEvent } from 'react';
import {Alert, Button, Form} from 'react-bootstrap';
import { useHistory } from 'react-router-dom';
import {LabRequest} from '../../models/LabRequest';
import { LabService } from '../../services/LabService';
import DatePicker from "react-datepicker";

import "react-datepicker/dist/react-datepicker.css";

const LabForm: React.FunctionComponent = () => {
    const labService = new LabService();
    const history = useHistory();

    const [labTypes, setLabTypes] = useState<string[]>([]);

    useEffect(() => {
        const getLabTypes = async () => {
            const l = await labService.getLabTypes();
            setLabTypes(l);
        }
        getLabTypes();
    }, [])

    const [validated, setValidated] = useState(false)

    const getDateAfterGivenDays = (days: number) => {
        const date = new Date();
        date.setDate(date.getDate() + days);
        return date;
    }
    
    const [selectedStartDate, setSelectedStartDate] = useState(getDateAfterGivenDays(1))

    const [selectedExpirationDate, setSelectedExpirationDate] = useState(getDateAfterGivenDays(7))

    const [errorMessage, setErrorMessage] = useState('')

    const handleStartDateChange = (date: any) => {
        setSelectedStartDate(date)
        setErrorMessage('')
    }

    const handleExpirationDateChange = (date: any) => {
        setSelectedExpirationDate(date)
        setErrorMessage('')
    }

    const [virtualMachines, setVirtualMachines] = useState(new Array(''));
    const [disableNewMachineButton, setDisableNewMachineButton] = useState(false);

    const addMachine = () => {
        const vm_count = virtualMachines.length;
        setVirtualMachines([...virtualMachines, '']);
        if(virtualMachines.length === 2)
            setDisableNewMachineButton(true);
    }

    const submitHandler = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();

        const MS_PER_MINUTE = 60000;
        if (new Date(new Date().getTime() - 5 * MS_PER_MINUTE) > selectedStartDate || selectedStartDate > selectedExpirationDate){
            setErrorMessage('Given dates are invalid. Please try again');
            event.stopPropagation();
            return;
        }

        const form = event.currentTarget as HTMLFormElement;
        if(!form.checkValidity()){
            event.stopPropagation();
            setValidated(true);
            return;
        }
        const nameInput = form.elements.namedItem('name') as HTMLInputElement;
        const typeInput = form.elements.namedItem('lab_type') as HTMLSelectElement;
        const descriptionInput = form.elements.namedItem('description') as HTMLInputElement;

        for(let i=0; i<virtualMachines.length; i++){
            const machineInput = form.elements.namedItem(`node-${i}`) as HTMLInputElement;
            virtualMachines[i] = machineInput.value;
        }

        const labService = new LabService();
        const createRequest = {
            lab_name: nameInput.value,
            lab_type: typeInput.value,
            start_date: selectedStartDate.toISOString(),
            expiration_date: selectedExpirationDate.toISOString(),
            description: descriptionInput.value,
            machines: virtualMachines
        } as LabRequest;

        await labService.createLab(createRequest);
        
        history.push('/labs');
    }
    
    return (
        <div className="lab-form">
            <h2>Create a new lab</h2>
            {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}
            <Form noValidate validated={validated} onSubmit={submitHandler}>
                <Form.Group controlId="formLabName">
                    <Form.Label>Lab name</Form.Label>
                    <Form.Control className="lab-form-input" type="text"
                                  name="name" placeholder="Enter lab name" required/>
                    <Form.Control.Feedback type="invalid">Please enter a lab name</Form.Control.Feedback>
                </Form.Group>

                <Form.Group>
                    <Form.Label>Lab type</Form.Label>
                    <Form.Control className="lab-form-input" as="select" name="lab_type" required>
                        {labTypes.map((labType, index) => (
                            <option key={index}>{labType}</option>
                        ))}
                    </Form.Control>
                </Form.Group>

                <Form.Group>
                    <Form.Label>Start date</Form.Label> <br/>
                      <DatePicker
                          className="date-input"
                          dateFormat="yyyy-MM-dd h:mm aa"
                          minDate={new Date()}
                          selected={selectedStartDate}
                          onChange={date => handleStartDateChange(date)}
                          showTimeInput
                      />
                      <br/>
                </Form.Group>

                <Form.Group>
                    <Form.Label>Expiration date</Form.Label> <br/>
                      <DatePicker
                          className="date-input"
                          dateFormat="yyyy-MM-dd h:mm aa"
                          minDate={new Date()}
                          selected={selectedExpirationDate}
                          onChange={date => handleExpirationDateChange(date)}
                          showTimeInput
                      />
                      <br/>
                </Form.Group>

                <Form.Group>
                    <Form.Label>Description</Form.Label>
                    <Form.Control className="lab-form-input" type="text"
                                  name="description" placeholder="Enter description" />
                </Form.Group>

                <Form.Group>
                    <Form.Label>Virtual Machines</Form.Label>
                    {virtualMachines.map((machine, index) => (
                        <Form.Control className="lab-form-input" type="text"
                                      key={index} name={`node-${index}`}
                                      placeholder="Enter machine name" required>
                        </Form.Control>
                    ))}
                    <Button variant="primary" onClick={addMachine} disabled={disableNewMachineButton}>
                        Add next machine
                    </Button>
                </Form.Group>

                <Button variant="primary" type="submit">
                    Create
                </Button>
            </Form>
        </div>
    );
}

export default LabForm;
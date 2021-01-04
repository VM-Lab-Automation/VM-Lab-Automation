import React from 'react'
import {Button} from "react-bootstrap";
import apiPaths from '../../services/APIPaths';
import { getAuthToken } from '../../services/AuthToken';

interface Props {
  lab_id: string;
}

const LabFilesButton: React.FunctionComponent<Props> = ({
    lab_id
    }: Props) => {

    return (
        <Button href={`${apiPaths.labFiles(lab_id)}?token=${getAuthToken()}`}>Download files</Button>
    );
}

export default LabFilesButton;
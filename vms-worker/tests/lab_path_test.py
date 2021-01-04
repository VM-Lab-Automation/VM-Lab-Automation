from worker.labs.lab_path import LabPath
from unittest.mock import patch, mock_open, MagicMock


@patch('os.path.isdir')
@patch('os.mkdir')
def test_lab_path_should_return_correct_userdata_when_is_already_a_dir(mkdir, isdir):
    lab_path = LabPath('/base')
    isdir.return_value = True

    data_folder = lab_path.get_data_folder()

    assert data_folder == '/base/userdata'
    assert mkdir.call_count == 0


@patch('os.path.isdir')
@patch('os.mkdir')
def test_lab_path_should_return_correct_userdata_and_create_when_is_not_a_dir(mkdir, isdir):
    lab_path = LabPath('/base')
    isdir.return_value = False

    data_folder = lab_path.get_data_folder()

    assert data_folder == '/base/userdata'
    assert mkdir.call_count == 2


@patch('os.utime')
@patch('os.path.isdir')
@patch('os.mkdir')
@patch('builtins.open', new_callable=mock_open, read_data='{ "key1": "val1", "key2": "val2" }')
def test_lab_path_should_return_correct_userdata_and_create_when_is_not_a_dir(open: MagicMock, mkdir, isdir, utime):
    lab_path = LabPath('/base')
    isdir.return_value = True

    info = lab_path.get_info()

    assert open.call_count == 2
    assert info == {'key1': 'val1', 'key2': 'val2'}
    open.assert_called_with('/base/lab.json', 'r')

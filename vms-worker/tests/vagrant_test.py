from unittest.mock import patch

from worker.vagrant.vagrant import Vagrant


@patch('subprocess.Popen')
def test_vagrant_up(popen):
    popen.return_value.communicate.return_value = bytes('test_out', encoding='UTF-8'), bytes('test_err', encoding='UTF-8')
    popen.return_value.returncode = 4
    vagrant = Vagrant('/path', 2)

    result_return_code, result_command, result_out, result_err = vagrant.up()

    assert result_return_code == 4
    assert result_command == 'bash -c "cd /path && VM_COUNT=2 vagrant up "'
    assert result_out == 'test_out'
    assert result_err == 'test_err'

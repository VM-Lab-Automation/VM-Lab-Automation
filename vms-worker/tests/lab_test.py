from unittest.mock import patch, MagicMock

from pytest import fixture

from worker.labs.lab import Lab


@fixture()
def lab_fixture():
    with patch('worker.labs.lab.LabPath') as lab_path:
        with patch('worker.labs.lab.Vagrant') as vagrant:
            with patch('os.getenv') as getenv:
                with patch('os.path.abspath') as abspath:
                    lab_path.return_value.get_info.return_value = {
                        'status': 'running',
                        'provider': 'VirtualBox'
                    }
                    getenv.return_value = '/base'
                    yield Lab('idik'), lab_path.return_value, vagrant.return_value, abspath


def test_init_lab(lab_fixture):
    lab, lab_path, vagrant, abspath = lab_fixture
    assert lab.lab_path == lab_path
    assert lab.vagrant == vagrant
    abspath.assert_called_with('/base/idik')


def test_status_when_not_include_machines_and_all_running(lab_fixture):
    lab, lab_path, vagrant, abspath = lab_fixture

    lab_path.get_info.return_value = {
        'status': 'RUNNING',
        'template': 'BASE',
        'vm_count': 1,
        'start_date': '2020-12-28T20:26:00.000000Z',
        'expiration_date': '2021-01-04T20:24:34.421000Z',
        'provider': 'VirtualBox'
    }
    vagrant.status.return_value = [
        ('node-1', 'running')
    ]

    result = lab.status(include_machines=False)

    assert result == {
        'expiration_date': '2021-01-04T20:24:34.421000Z',
        'lab_id': 'idik',
        'provider': 'VirtualBox',
        'start_date': '2020-12-28T20:26:00.000000Z',
        'status': 'RUNNING',
        'template': 'BASE',
        'vm_count': 1
    }


def test_status_when_not_include_machines_and_not_all_running(lab_fixture):
    lab, lab_path, vagrant, abspath = lab_fixture

    lab_path.get_info.return_value = {
        'status': 'RUNNING',
        'template': 'BASE',
        'vm_count': 1,
        'start_date': '2020-12-28T20:26:00.000000Z',
        'expiration_date': '2021-01-04T20:24:34.421000Z',
        'provider': 'VirtualBox'
    }
    vagrant.status.return_value = [
        ('node-1', 'not running'),
        ('node-2', 'running')
    ]

    result = lab.status(include_machines=False)

    assert result == {
        'expiration_date': '2021-01-04T20:24:34.421000Z',
        'lab_id': 'idik',
        'provider': 'VirtualBox',
        'start_date': '2020-12-28T20:26:00.000000Z',
        'status': 'PARTIALLY_RUNNING',
        'template': 'BASE',
        'vm_count': 1
    }


def test_status_when_not_include_machines_and_nothing_running(lab_fixture):
    lab, lab_path, vagrant, abspath = lab_fixture

    lab_path.get_info.return_value = {
        'status': 'RUNNING',
        'template': 'BASE',
        'vm_count': 1,
        'start_date': '2020-12-28T20:26:00.000000Z',
        'expiration_date': '2021-01-04T20:24:34.421000Z',
        'provider': 'VirtualBox'
    }
    vagrant.status.return_value = [
        ('node-1', 'not running'),
        ('node-2', 'not running')
    ]

    result = lab.status(include_machines=False)

    assert result == {
        'expiration_date': '2021-01-04T20:24:34.421000Z',
        'lab_id': 'idik',
        'provider': 'VirtualBox',
        'start_date': '2020-12-28T20:26:00.000000Z',
        'status': 'NOT_RUNNING',
        'template': 'BASE',
        'vm_count': 1
    }


def test_status_when_include_machines(lab_fixture):
    lab, lab_path, vagrant, abspath = lab_fixture

    lab_path.get_info.return_value = {
        'status': 'RUNNING',
        'template': 'BASE',
        'vm_count': 1,
        'start_date': '2020-12-28T20:26:00.000000Z',
        'expiration_date': '2021-01-04T20:24:34.421000Z',
        'provider': 'VirtualBox'
    }
    vagrant.status.return_value = [
        ('node-1', 'running'),
        ('node-2', 'not running')
    ]
    vagrant.ports.return_value = [
        (3387, 3389),
        (2222, 22),
        (45, 67)
    ]

    result = lab.status()

    assert result == {
        'expiration_date': '2021-01-04T20:24:34.421000Z',
        'lab_id': 'idik',
        'provider': 'VirtualBox',
        'start_date': '2020-12-28T20:26:00.000000Z',
        'status': 'PARTIALLY_RUNNING',
        'template': 'BASE',
        'vm_count': 1,
        'machines': [
            {'login': 'root', 'name': 'node-1', 'password': 'root', 'rdp_port': 3387, 'ssh_port': 2222, 'status': 'running'},
            {'login': 'root', 'name': 'node-2', 'password': 'root', 'rdp_port': 3387, 'ssh_port': 2222, 'status': 'not running'}
        ]
    }

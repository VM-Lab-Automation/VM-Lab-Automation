import subprocess


class Vagrant:

    def __init__(self, path, vm_count):
        self.path = path
        self.vm_count = vm_count

    @staticmethod
    def __execute__command(command):
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        return proc.returncode, str(out, "utf-8") if out is not None else None, str(err,  "utf-8") if err is not None else None

    def up(self, args=None):
        if args is None:
            args = []
        command = 'bash -c "cd {0} && VM_COUNT={1} vagrant up {2}"'\
            .format(self.path, self.vm_count, ' '.join(args))
        return_code, out, err = self.__execute__command(command)
        return return_code, command, out, err

    def status(self) -> [(str, str, str)]:
        command = 'bash -c "cd {0} && VM_COUNT={1} vagrant status --machine-readable"'.format(self.path, self.vm_count)
        return_code, out, _ = self.__execute__command(command)
        lines = out.split('\n')
        splitted_lines = [l.split(',') for l in lines]
        status = [(l[1], l[3]) for l in splitted_lines if len(l) > 2 and l[2] == 'state']
        return status

    def ports(self, machine) -> [(int, int)]:
        return []

    def destroy(self):
        command = 'bash -c "cd {0} && VM_COUNT={1} vagrant destroy -f"'.format(self.path, self.vm_count)
        return_code, out, err = self.__execute__command(command)
        return return_code, command, out, err

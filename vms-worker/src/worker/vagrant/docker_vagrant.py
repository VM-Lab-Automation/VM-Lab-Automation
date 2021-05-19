import subprocess


class DockerVagrant:

    def __init__(self, path, vm_count):
        self.vm_count = vm_count
        self.path = path

    @staticmethod
    def __execute__command(command):
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        return proc.returncode, str(out, "utf-8") if out is not None else None, str(err,  "utf-8") if err is not None else None

    def up(self, args=None):
        if args is None:
            args = []
        command = 'bash -c "cd {0} && VM_COUNT={1} vagrant up {2} --provider docker"'\
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
        vagrant_directory = self.path.split('/')[-1]
        filter = "name={}".format("{}_{}".format(vagrant_directory, machine))
        command = 'docker ps -a --filter %s --format "{{.Names}};{{.Ports}}"' % filter
        return_code, line, _ = self.__execute__command(command)
        ports_redirects_str = line.split(';')[1].split(',') if line != '' else []
        ports_splitted = [ l.split('->') for l in ports_redirects_str]

        def clean_port(port_str: str):
            port = port_str.strip().split('/')[0]
            if ':' in port:
                port = port[port.rfind(':')+1:]
            try:
                return int(port) if port != '' else 0   
            except:
                return 0

        return [(clean_port(p[0]) if len(p) > 0 else 0, clean_port(p[1]) if len(p)>1 else 0) for p in ports_splitted]

    def destroy(self):
        command = 'bash -c "cd {0} && VM_COUNT={1} vagrant destroy -f"'.format(self.path, self.vm_count)
        return_code, out, err = self.__execute__command(command)
        return return_code, command, out, err

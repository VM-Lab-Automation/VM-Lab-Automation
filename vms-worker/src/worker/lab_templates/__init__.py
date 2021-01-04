import json
import os

lab_templates_path = os.getenv("LAB_TEMPLATES_PATH")


class LabTemplate:

    def __init__(self, codename, path, provider):
        self.path = path
        self.codename = codename
        self.provider = provider


class LabTemplatesRepository:

    def get_all(self) -> [LabTemplate]:
        dir_content = os.listdir(lab_templates_path)
        paths = [os.path.join(lab_templates_path, d) for d in dir_content if not d.startswith('.')]
        valid_dirs = [d for d in paths if os.path.isdir(d)]
        jsons = [(json.loads(open("{}/lab_template.json".format(d), "r").read()), d) for d in valid_dirs]
        return [LabTemplate(j['code'], d, j['provider']) for (j, d) in jsons]

    def get(self, codename) -> LabTemplate:
        templates = self.get_all()
        template = [t for t in templates if t.codename == codename]
        if len(template) == 0:
            raise Exception('Lab template not found')
        return template[0]

from mock import MagicMock

from logic.lab_templates_service import LabTemplatesService
from models.lab_template import LabTemplate


def test_get_templates_name_should_return_templates_name():
    templates_repository = MagicMock()

    templates = [
        LabTemplate("id1", "code1", "name1"),
        LabTemplate("id2", "code2", "name2"),
        LabTemplate("id3", "code3", "name3")
    ]

    templates_repository.get_all.return_value = templates

    templates_service = LabTemplatesService(templates_repository)
    assert templates_service.get_templates_name() == [template.lab_name for template in templates]

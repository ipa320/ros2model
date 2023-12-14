import unittest
import yaml

from ros2model.core.generator.file_generator import FileGenerator
from pathlib import Path

test_dir = "test"
template_dir = "resource/templates"
template_file = "test_template.j2"
output_folder = "outputs"
output_file = "test.yaml"

test_yaml_content = """
name: builtin_interfaces
fromGitRepo: git_repo
"""


class test_jinja_generator(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = Path(test_dir)
        self.template_dir = Path(self.test_dir / template_dir).resolve()
        self.template_path = Path(self.template_dir / template_file).resolve()
        self.test_model = yaml.safe_load(test_yaml_content)
        self.output_dir = Path(self.test_dir / output_folder)

    def test_file_exists(self):
        self.assertTrue(self.template_dir.is_dir())
        self.assertTrue(self.template_path.is_file())

    def test_generate_template_file(self):
        generator = FileGenerator(self.output_dir)
        generator.generate_file(self.template_path, output_file, model=self.test_model)
        with open(Path(self.output_dir / output_file), "r") as file:
            data = yaml.safe_load(file)
        self.assertEqual(self.test_model, data)


if __name__ == "__main__":
    unittest.main()

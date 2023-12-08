from TableauConMan.sources.specification_source import SpecificationSource
import tableauserverclient as TSC
import unittest
import unittest.mock as mock
import json

TEST_SPECIFICATION_FILE = {"file_path": "./tests/assets/simple_specification.yaml"}

TEST_SPECIFICATION_JSON = {
    "version": "1.0",
    "projects": [
        {
            "project_name": "Test Project",
            "description": "This project includes automatically uploaded samples.",
            "content_permissions": "LockedToProject",
            "project_path": "Test Project",
            "permission_set": [{"group_name": "Test Group", "permission_rule": "view"}],
        }
    ],
    "permission_templates": [
        {"name": "view", "workbook": {"Read": "Allow"}, "datasource": {"Read": "Allow"}}
    ],
    "groups": [{"group_name": "Test Group"}, {"group_name": "Test Group Two"}],
}

TEST_PERMISSION_TEMPLATE_OUTPUT = {
    "projects": [
        {
            "project_name": "Test Project",
            "description": "This project includes automatically uploaded samples.",
            "content_permissions": "LockedToProject",
            "project_path": "Test Project",
            "permission_set": [
                {
                    "group_name": "Test Group",
                    "permission_rule": "aff2bc700bf610448584b377da6598fc",
                }
            ],
        }
    ],
    "permission_templates": [
        {
            "name": "aff2bc700bf610448584b377da6598fc",
            "workbook": {"Read": "Allow"},
            "datasource": {"Read": "Allow"},
        }
    ],
}

TEST_PERMISSION_TEMPLATE_INPUT = [
    {
        "project_name": "Test Project",
        "description": "This project includes automatically uploaded samples.",
        "content_permissions": "LockedToProject",
        "project_path": "Test Project",
        "permission_set": [
            {
                "group_name": "Test Group",
                "permission_rule": {
                    "workbook": {"Read": "Allow"},
                    "datasource": {"Read": "Allow"},
                },
            }
        ],
    }
]


class TestSpecificationSource(unittest.TestCase):
    def setUp(self) -> None:
        ...

    def test_load(self):
        expected_json = {
            "file_path": "./tests/assets/simple_specification.yaml",
            "source_type": "specification",
        }

        test_source = SpecificationSource().load(source_config=TEST_SPECIFICATION_FILE)

        self.assertEqual(expected_json, test_source.__dict__)

    def test_read_yaml(self):
        expected_json = TEST_SPECIFICATION_JSON

        test_source = SpecificationSource().load(source_config=TEST_SPECIFICATION_FILE)

        test_json = test_source.read_yaml()

        # self.maxDiff = None

        self.assertEqual(
            json.dumps(
                expected_json,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=4,
            ),
            json.dumps(
                test_json, default=lambda o: o.__dict__, sort_keys=True, indent=4
            ),
        )

    def test_get_asset(self):
        expected_json = [
            {
                "project_name": "Test Project",
                "description": "This project includes automatically uploaded samples.",
                "content_permissions": "LockedToProject",
                "project_path": "Test Project",
                "permission_set": [
                    {
                        "group_name": "Test Group",
                        "permission_rule": {
                            "workbook": {"Read": "Allow"},
                            "datasource": {"Read": "Allow"},
                        },
                    }
                ],
            }
        ]

        test_source = SpecificationSource().load(source_config=TEST_SPECIFICATION_FILE)

        self.maxDiff = None

        test_json = test_source.get_assets("projects")

        self.assertEqual(
            json.dumps(
                expected_json,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=4,
            ),
            json.dumps(
                test_json, default=lambda o: o.__dict__, sort_keys=True, indent=4
            ),
        )

    def test_write_permission_templates(self):
        expected_output = TEST_PERMISSION_TEMPLATE_OUTPUT

        expected_project_list = expected_output.get("projects")

        expected_permission_templates = {
            key: value
            for key, value in expected_output.items()
            if key == "permission_templates"
        }

        test_source = SpecificationSource()

        test_file, test_project_list = test_source.write_permission_templates(
            dict(), TEST_PERMISSION_TEMPLATE_INPUT
        )

        self.maxDiff = None

        self.assertEqual(
            json.dumps(
                expected_permission_templates,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=4,
            ),
            json.dumps(
                test_file,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=4,
            ),
        )

        self.assertEqual(
            json.dumps(
                expected_project_list,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=4,
            ),
            json.dumps(
                test_project_list,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=4,
            ),
        )

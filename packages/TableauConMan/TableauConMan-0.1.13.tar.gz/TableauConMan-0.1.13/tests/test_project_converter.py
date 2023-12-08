from TableauConMan.assets.project_asset import Project
import tableauserverclient as TSC
import unittest
import unittest.mock as mock
import json
from TableauConMan.assets.permission_rule_asset import PermissionRule
from TableauConMan.converters.project_converter import ProjectConverter
from TableauConMan.sources.server_source import ServerSource
import TableauConMan.config.plan_options as options


TEST_GROUP_ONE = TSC.GroupItem("Test Group")
TEST_GROUP_ONE._id = 123456789

TEST_GROUP_TWO = TSC.GroupItem("Test Group 2")
TEST_GROUP_TWO._id = 987654321

SERVER_GROUPS = [TEST_GROUP_ONE, TEST_GROUP_TWO]

TEST_SERVER_PROJECT_ONE = TSC.ProjectItem(
    name="Test Project 1",
    description="Test Project 1 Description",
    content_permissions="LockedToProjectWithoutNested",
    parent_id=None,
)

TEST_SERVER_PROJECT_TWO = TSC.ProjectItem(
    name="Test Project 2",
    description="Test Project 2 Description",
    content_permissions="LockedToProject",
    parent_id=123456789,
)

"""TSC.ProjectItem(
            name="Test Project 2",
            description="Test Project 2 Description",
            content_permissions="LockedToProject",
            parent_id=123456789,
        )

        expected_server_project_item._default_workbook_permissions = list(
            [
                TSC.PermissionsRule(
                    grantee=TEST_GROUP_TWO, capabilities=dict({"Read": "Alow"})
                )
            ]
        )"""


TEST_SERVER_PROJECT_ONE._id = 123456789
TEST_SERVER_PROJECT_TWO._id = 987654321

TEST_SERVER_PROJECT_TWO._default_workbook_permissions = list(
    [
        TSC.PermissionsRule(
            grantee=TEST_GROUP_TWO, capabilities=dict({"Read": "Alow"})
        ),
    ]
)
TEST_SERVER_PROJECT_TWO._default_datasource_permissions = list(
    [
        TSC.PermissionsRule(
            grantee=TEST_GROUP_TWO, capabilities=dict({"Read": "Alow"})
        ),
    ]
)
SERVER_PROJECTS = [
    TEST_SERVER_PROJECT_ONE,
    TEST_SERVER_PROJECT_TWO,
]

TEST_SPECIFICATION_PROJECT_TWO = dict(
    {
        "project_name": "Test Project 2",
        "description": "Test Project 2 Description",
        "content_permissions": "LockedToProject",
        "project_path": "Test Project 1/Test Project 2",
        "permission_set": [
            {
                "group_name": "Test Group 2",
                "permission_rule": {
                    "workbook": {"Read": "Alow"},
                    "datasource": {"Read": "Alow"},
                },
            }
        ],
    }
)

TEST_SPECIFICATION_PROJECT_ONE = dict(
    {
        "project_name": "Test Project 1",
        "description": "Test Project 1 Description",
        "content_permissions": "LockedToProjectWithoutNested",
        "project_path": "Test Project 1",
        "permission_set": [
            {
                "group_name": "Test Group 2",
                "permission_rule": {
                    "workbook": {"Read": "Alow"},
                    "datasource": {"Read": "Alow"},
                },
            }
        ],
    }
)

SPECIFICATION_PROJECTS = [
    TEST_SPECIFICATION_PROJECT_ONE,
    TEST_SPECIFICATION_PROJECT_TWO,
]

""""permission_set": [
            {
                "group_name": "Test Group 2",
                "permission_rule": {
                    "workbook": {"Read": "Alow"},
                    "datasource": {"Read": "Alow"},
                },
            }
        ],"""

TEST_ASSET_PROJECT_TWO = Project(
    project_id=987654321,
    project_path="Test Project 1/Test Project 2",
    project_parent_id=123456789,
    project_name="Test Project 2",
    description="Test Project 2 Description",
    content_permissions="LockedToProject",
    parent_content_permissions="LockedToProjectWithoutNested",
    permission_set=list(
        [
            PermissionRule(
                asset_type="workbook",
                grantee_type="group",
                grantee_name="Test Group 2",
                capabilities=dict({"Read": "Alow"}),
            ),
            PermissionRule(
                asset_type="datasource",
                grantee_type="group",
                grantee_name="Test Group 2",
                capabilities=dict({"Read": "Alow"}),
            ),
        ]
    ),
)

TEST_ASSET_PROJECT_ONE = Project(
    project_id=123456789,
    project_path="Test Project 1",
    project_parent_id="",
    project_name="Test Project 1",
    description="Test Project 1 Description",
    content_permissions="LockedToProjectWithoutNested",
    parent_content_permissions="",
)

""""""


def get_test_server_project_two():
    return TEST_SERVER_PROJECT_TWO


def server_args_based_return(*args, **kwargs):
    if args[0] == "projects":
        return SERVER_PROJECTS
    elif args[0] == "groups":
        return SERVER_GROUPS
    else:
        return Exception("exception occurred")


def specification_args_based_return(*args, **kwargs):
    if args[0] == "projects":
        return SPECIFICATION_PROJECTS
    elif args[0] == "groups":
        return SERVER_GROUPS
    else:
        return Exception("exception occurred")


class MockServerSource(ServerSource):
    pass


class TestProjectConverter(unittest.TestCase):
    @mock.patch("TableauConMan.sources.specification_source.SpecificationSource")
    @mock.patch("TableauConMan.sources.server_source.ServerSource")
    def setUp(self, mock_server, mock_specification) -> None:
        # mock_server.get_assets.return_value = args_based_return
        mock_server.get_assets.side_effect = server_args_based_return
        mock_server.source_type = "server"
        mock_specification.get_assets.side_effect = specification_args_based_return
        mock_specification.source_type = "specification"

        self.test_converter = ProjectConverter(mock_server)
        self.test_converter_specification = ProjectConverter(mock_specification)
        self.maxDiff = None

        options.INCLUDE_ASSET_PERMISSIONS = True

        # assert mock_server.get_assets("groups") == SERVER_GROUPS
        # assert mock_server.get_assets("projects") == SERVER_PROJECTS

    def test_convert_to_asset(self):
        """Having a hard time setting up the code to it can both run and be tested. The class property tests is a function can calls the server."""
        # expected_asset = TEST_ASSET_PROJECT_TWO

        # test_server_item = self.test_converter.convert_to_asset(TEST_SERVER_PROJECT_TWO)

        # self.assertEqual(expected_asset.__dict__, test_server_item.__dict__)

    def test_convert_to_source(self):
        expected_asset = TEST_SERVER_PROJECT_ONE

        test_asset = self.test_converter.convert_to_source(TEST_ASSET_PROJECT_ONE)

        self.assertEqual(
            json.dumps(
                expected_asset,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=4,
            ),
            json.dumps(
                test_asset, default=lambda o: o.__dict__, sort_keys=True, indent=4
            ),
        )

    def test_asset_to_server(self):
        expected_server_project_item = TSC.ProjectItem(
            name="Test Project 2",
            description="Test Project 2 Description",
            content_permissions="LockedToProject",
            parent_id=123456789,
        )
        expected_server_project_item._id = ""

        expected_server_project_item._default_workbook_permissions = list(
            [
                TSC.PermissionsRule(
                    grantee=TEST_GROUP_TWO, capabilities=dict({"Read": "Alow"})
                )
            ]
        )

        expected_server_project_item._default_datasource_permissions = list(
            [
                TSC.PermissionsRule(
                    grantee=TEST_GROUP_TWO, capabilities=dict({"Read": "Alow"})
                )
            ]
        )

        test_asset = Project(
            project_id="",
            project_path="Test Project 1/Test Project 2",
            project_parent_id="",
            project_name="Test Project 2",
            description="Test Project 2 Description",
            content_permissions="LockedToProject",
            parent_content_permissions="LockedToProjectWithoutNested",
            permission_set=list(
                [
                    PermissionRule(
                        asset_type="workbook",
                        grantee_type="group",
                        grantee_name="Test Group 2",
                        capabilities=dict({"Read": "Alow"}),
                    ),
                    PermissionRule(
                        asset_type="datasource",
                        grantee_type="group",
                        grantee_name="Test Group 2",
                        capabilities=dict({"Read": "Alow"}),
                    ),
                ]
            ),
        )

        test_server_item = self.test_converter.asset_to_server(test_asset)

        self.assertEqual(
            json.dumps(
                expected_server_project_item,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=4,
            ),
            json.dumps(
                test_server_item, default=lambda o: o.__dict__, sort_keys=True, indent=4
            ),
        )

    def test_asset_to_specification(self):
        expected_server_item = TEST_SPECIFICATION_PROJECT_TWO

        test_asset = Project(
            project_id="",
            project_path="Test Project 1/Test Project 2",
            project_parent_id=123456789,
            project_name="Test Project 2",
            description="Test Project 2 Description",
            content_permissions="LockedToProject",
            parent_content_permissions="LockedToProjectWithoutNested",
            permission_set=list(
                [
                    PermissionRule(
                        asset_type="workbook",
                        grantee_type="group",
                        grantee_name="Test Group 2",
                        capabilities=dict({"Read": "Alow"}),
                    ),
                    PermissionRule(
                        asset_type="datasource",
                        grantee_type="group",
                        grantee_name="Test Group 2",
                        capabilities=dict({"Read": "Alow"}),
                    ),
                ]
            ),
        )

        test_server_item = self.test_converter.asset_to_specification(test_asset)

        self.assertEqual(
            json.dumps(
                expected_server_item,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=4,
            ),
            json.dumps(
                test_server_item,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=4,
            ),
        )

    def test_server_to_asset(self):
        """Having a hard time setting up the code to it can both run and be tested. The class property tests is a function can calls the server."""
        expected_asset = Project(
            project_id=987654321,
            project_path="Test Project 1/Test Project 2",
            project_parent_id=123456789,
            project_name="Test Project 2",
            description="Test Project 2 Description",
            content_permissions="LockedToProject",
            parent_content_permissions="LockedToProjectWithoutNested",
            permission_set=list(
                [
                    PermissionRule(
                        asset_type="workbook",
                        grantee_type="group",
                        grantee_name="Test Group 2",
                        capabilities=dict({"Read": "Alow"}),
                    ),
                    PermissionRule(
                        asset_type="datasource",
                        grantee_type="group",
                        grantee_name="Test Group 2",
                        capabilities=dict({"Read": "Alow"}),
                    ),
                ]
            ),
        )

        # test_server_item = self.test_converter.server_to_asset(TEST_SERVER_PROJECT_TWO)

        """self.assertEqual(
            json.dumps(
                expected_asset,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=4,
            ),
            json.dumps(
                test_server_item,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=4,
            ),
        )"""

    def test_specification_to_asset(self):
        expected_asset = Project(
            project_id="",
            project_path="Test Project 1/Test Project 2",
            project_parent_id="",
            project_name="Test Project 2",
            description="Test Project 2 Description",
            content_permissions="LockedToProject",
            parent_content_permissions="LockedToProjectWithoutNested",
            permission_set=list(
                [
                    PermissionRule(
                        asset_type="workbook",
                        grantee_type="group",
                        grantee_name="Test Group 2",
                        capabilities=dict({"Read": "Alow"}),
                    ),
                    PermissionRule(
                        asset_type="datasource",
                        grantee_type="group",
                        grantee_name="Test Group 2",
                        capabilities=dict({"Read": "Alow"}),
                    ),
                ]
            ),
        )

        """"""

        test_item = TEST_SPECIFICATION_PROJECT_TWO

        test_asset = self.test_converter_specification.specification_to_asset(test_item)

        self.assertEqual(
            json.dumps(
                expected_asset,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=4,
            ),
            json.dumps(
                test_asset,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=4,
            ),
        )

    def test_project_path_id_map(self):
        expected_project_id_map = dict(
            {"Test Project 1": 123456789, "Test Project 1/Test Project 2": 987654321}
        )

        test_project_id_map = self.test_converter._get_project_path_id_map()

        self.assertEqual(expected_project_id_map, test_project_id_map)

    def test_get_project_path(self):
        expected_project_path = "Test Project 1/Test Project 2"

        test_server_item_id = TEST_SERVER_PROJECT_TWO.id

        test_project_path = self.test_converter._get_project_path(
            test_server_item_id, self.test_converter.project_path_id_map
        )

        self.assertEqual(expected_project_path, test_project_path)

    def test_get_project_parent_id(self):
        expected_project_parent_id = 123456789

        test_project_path = "Test Project 1/Test Project 2"

        test_project_parent_id = self.test_converter._get_project_parent_id(
            test_project_path, self.test_converter.project_path_id_map
        )

        self.assertEqual(expected_project_parent_id, test_project_parent_id)


if __name__ == "__main__":
    unittest.main()

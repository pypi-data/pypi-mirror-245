from TableauConMan.assets.permission_rule_asset import PermissionRule
import tableauserverclient as TSC
import unittest
import unittest.mock as mock
from TableauConMan.converters.permission_rule_converter import PermissionRuleConverter


TEST_GROUP_ONE = TSC.GroupItem("Test Group")
TEST_GROUP_ONE._id = 123456789

TEST_GROUP_TWO = TSC.GroupItem("Test Group 2")
TEST_GROUP_TWO._id = 987654321

SERVER_GROUPS = [TEST_GROUP_ONE, TEST_GROUP_TWO]


class TestPermissionRuleConverter(unittest.TestCase):
    @mock.patch("TableauConMan.sources.server_source.ServerSource")
    def setUp(self, mock_server) -> None:
        mock_server.get_assets.return_value = SERVER_GROUPS
        self.test_converter = PermissionRuleConverter(mock_server)

    def test_asset_to_server(self):
        expected_server_item = TSC.PermissionsRule(
            grantee=TEST_GROUP_ONE,
            capabilities=dict({"Read": "Alow"}),
        )

        test_asset = PermissionRule(
            asset_type="workbook",
            grantee_type="group",
            grantee_name="Test Group",
            capabilities=dict({"Read": "Alow"}),
        )

        test_server_item = self.test_converter.asset_to_server(test_asset)

        self.assertEqual(expected_server_item.__dict__, test_server_item.__dict__)

    def test_asset_to_specification(self):
        expected_specification_item = dict(
            {
                "group_name": "Test Group",
                "permission_rule": dict({"workbook": dict({"Read": "Alow"})}),
            }
        )

        test_asset = PermissionRule(
            asset_type="workbook",
            grantee_type="group",
            grantee_name="Test Group",
            capabilities=dict({"Read": "Alow"}),
        )

        test_specification_item = self.test_converter.asset_to_specification(test_asset)

        self.assertEqual(expected_specification_item, test_specification_item)

    def test_server_to_asset(self):
        expected_asset = PermissionRule(
            asset_type="workbook",
            grantee_type="group",
            grantee_name="Test Group",
            capabilities=dict({"Read": "Alow"}),
        )

        test_server_item = TSC.PermissionsRule(
            grantee=TEST_GROUP_ONE,
            capabilities=dict({"Read": "Alow"}),
        )

        test_asset = self.test_converter.server_to_asset(test_server_item, "workbook")

        self.assertEqual(expected_asset.__dict__, test_asset.__dict__)

    def test_specification_to_asset(self):
        expected_asset = PermissionRule(
            asset_type="workbook",
            grantee_type="group",
            grantee_name="Test Group",
            capabilities=dict({"Read": "Alow"}),
        )

        test_specification = dict(
            {
                "group_name": "Test Group",
                "permission_rule": dict({"workbook": dict({"Read": "Alow"})}),
            }
        )

        test_asset = self.test_converter.specification_to_asset(
            test_specification, "workbook"
        )

        self.assertEqual(expected_asset.__dict__, test_asset.__dict__)

    def test_get_grantee_item(self):
        expected_result = TEST_GROUP_ONE

        test_output = self.test_converter._get_grantee_item(
            grantee_name="Test Group", grantee_type="group"
        )

        self.assertEqual(expected_result.__dict__, test_output.__dict__)


if __name__ == "__main__":
    unittest.main()

import tableauserverclient as TSC

TEST_SERVER_PROJECT_ONE = TSC.ProjectItem(
    name="Test Project 1",
    description="Test Project 1 Description",
    content_permissions="LockedToProject",
    parent_id=None,
)

TEST_SERVER_PROJECT_TWO = TSC.ProjectItem(
    name="Test Project 2",
    description="Test Project 2 Description",
    content_permissions="LockedToProject",
    parent_id=123456789,
)


TEST_SERVER_PROJECT_ONE._id = 123456789
TEST_SERVER_PROJECT_TWO._id = 987654321
SERVER_PROJECTS = [
    TEST_SERVER_PROJECT_ONE,
    TEST_SERVER_PROJECT_TWO,
]

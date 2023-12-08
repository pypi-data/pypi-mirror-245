from TableauConMan.assets.project_asset import Project

TEST_PROJECT_ASSET_ONE = Project(
    project_id="",
    project_path="Test Project 1",
    project_parent_id="",
    project_name="Test Project 1",
    description="Test Project 1 Description",
    content_permissions="LockedToProject",
)

TEST_PROJECT_ASSET_TWO = Project(
    project_id="",
    project_path="Test Project 1/Test Project 2",
    project_parent_id="",
    project_name="Test Project 2",
    description="Test Project 2 Description",
    content_permissions="LockedToProject",
)

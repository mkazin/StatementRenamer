from unittest.mock import patch
from statement_renamer.tasks.action import Action
from statement_renamer.tasks.disk_file_handler import DiskFileHandler


@patch('os.rename')
def test_rename_action(mock_rename):

    file_handler = DiskFileHandler()

    old_name = "bad file name"
    new_name = "myfile.pdf"
    rename_action = Action.create_rename_action(old_name, new_name)

    file_handler.handle(rename_action)

    mock_rename.assert_called_with(old_name, new_name)

@patch('os.remove')
def test_delete_action(mock_remove):

    file_handler = DiskFileHandler()

    file_to_delete = "bad file name"
    delete_action = Action.create_delete_action(file_to_delete)

    file_handler.handle(delete_action)

    mock_remove.assert_called_with(file_to_delete)

@patch('os.remove')
@patch('os.rename')
def test_ignore_action(mock_remove, mock_rename):
    ignore_action = Action.create_ignore_action("file to ignore", "unit test")

    file_handler = DiskFileHandler()

    file_handler.handle(ignore_action)

    mock_remove.assert_not_called()
    mock_rename.assert_not_called()
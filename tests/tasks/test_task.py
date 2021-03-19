from unittest import mock
# from mock import MagicMock
# thing = ProductionClass()
# thing.method = MagicMock(return_value=3)
# thing.method(3, 4, 5, key='value')

# thing.method.assert_called_with(3, 4, 5, key='value')

# from statement_renamer import containers
# from statement_renamer.containers import Container

def test_file_handler_called_on_delete_when_not_simulated():

    # container = Container()
    mock_file_handler = mock.Mock()
    mock_logger = mock.Mock()
    # container.logger.override(mock_logger)
    # container.file_handler.override(mock_file_handler)

    # service = container.service()


# def test_file_handler_not_called_on_delete_when_simulated():

# Task

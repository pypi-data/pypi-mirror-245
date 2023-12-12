from unittest.mock import patch


@patch("builtins.print")
def test_print_loggers(mock_print):
    """Test the print_loggers function."""
    from log2me.print_loggers import print_loggers

    print_loggers()
    assert mock_print.call_count == 8

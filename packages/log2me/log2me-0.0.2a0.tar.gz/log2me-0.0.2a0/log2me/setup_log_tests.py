import datetime
import os.path

from log2me.settings import LogSettings


def test_get_log_file(tmpdir, mocker):
    """Test the get_log_file function."""
    FAKE_TIME = datetime.datetime(2020, 12, 25, 17, 5, 55)
    mock_date = mocker.patch("log2me.setup_log.datetime")
    mock_date.now.return_value = FAKE_TIME

    from log2me.setup_log import get_log_file

    assert get_log_file(os.path.join(tmpdir, "%date%.log")).endswith(
        "2020-12-25.log"
    )
    assert get_log_file(os.path.join(tmpdir, "%time%.log")).endswith(
        "17-05-55.log"
    )
    assert get_log_file(os.path.join(tmpdir, "%Y%.log")).endswith("2020.log")
    assert get_log_file(os.path.join(tmpdir, "%M%.log")).endswith("12.log")
    assert get_log_file(os.path.join(tmpdir, "%D%.log")).endswith("25.log")
    assert get_log_file(os.path.join(tmpdir, "%H%.log")).endswith("17.log")
    assert get_log_file(os.path.join(tmpdir, "%m%.log")).endswith("5.log")
    assert get_log_file(os.path.join(tmpdir, "%s%.log")).endswith("55.log")
    assert get_log_file(os.path.join(tmpdir, "%ms%.log")).endswith("0.log")
    assert get_log_file(os.path.join(tmpdir, "log2me.log")).endswith(
        "log2me.log"
    )


def test_setup(tmpdir, mocker):
    from log2me.setup_log import setup_logging

    getLogger = mocker.patch("log2me.setup_log.logging.getLogger")
    top_logger = mocker.Mock()
    getLogger.return_value = top_logger

    setup_logging(LogSettings())
    assert getLogger.call_count == 2

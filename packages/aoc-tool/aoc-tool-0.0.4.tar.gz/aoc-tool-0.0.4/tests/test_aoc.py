import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from aoc_tool import get_input, submit

TEST_YEAR = 1000


@pytest.fixture(autouse=True)
def cleanup_files():
    try:
        p = Path(f"{os.environ['HOME']}/.cache/aoc_tool/infile_{TEST_YEAR}_1")
        p.unlink()
    except FileNotFoundError:
        pass


def test_get_input_no_cookie():
    if "AOC_COOKIE" in os.environ:
        del os.environ["AOC_COOKIE"]
    with pytest.raises(Exception):
        get_input(TEST_YEAR, 1)


def test_submit_no_cookie():
    if "AOC_COOKIE" in os.environ:
        del os.environ["AOC_COOKIE"]
    with pytest.raises(Exception):
        submit("foo", TEST_YEAR, 1, 1)


@patch("urllib.request.urlopen", autospec=True)
def test_get_input(mock_urlopen):
    os.environ["AOC_COOKIE"] = "cookie"
    mock = MagicMock()
    mock.read.return_value = b"Test data"
    mock.__enter__.return_value = mock
    mock_urlopen.return_value = mock

    data = get_input(TEST_YEAR, 1)
    mock_urlopen.assert_called_once()
    assert data == "Test data"

    data = get_input(TEST_YEAR, 1)
    mock_urlopen.assert_called_once()
    assert data == "Test data"


@patch("urllib.request.urlopen", autospec=True)
def test_submit(mock_urlopen, capsys):
    os.environ["AOC_COOKIE"] = "cookie"
    mock = MagicMock()
    mock.read.return_value = b"""
<html>
<body>
<article>
<p>Test data <a href="some_url">[Return]</a></p>
</article>
</body>
</html>
"""
    mock.__enter__.return_value = mock
    mock_urlopen.return_value = mock
    submit("foo", TEST_YEAR, 1, 1)
    mock_urlopen.assert_called_once()
    assert capsys.readouterr().out == "Test data [Return]\n"

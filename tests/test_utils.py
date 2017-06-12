import pytest

from roundhouse.utils import get_full_qualname, get_file_extension


@pytest.mark.parametrize('filepath,expected', [
    ('local.file', '.file'),
    ('file.double.ext', '.double.ext'),
    ('relative/path/to/file.txt', '.txt'),
    ('/absoloute/path/to/file.txt', '.txt')
])
def test_get_file_extension(filepath, expected):
    assert get_file_extension(filepath) == expected

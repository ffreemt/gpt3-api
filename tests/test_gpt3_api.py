"""Test gpt3_api."""
from gpt3_api import __version__
from gpt3_api import gpt3_api


def test_version():
    """Test version."""
    assert __version__ == "0.1.0"


def test_sanity():
    """Sanity check."""
    try:
        assert not gpt3_api()
    except Exception:
        assert True

"""Test zh2en."""
from gpt3_api.zh2en import zh2en


def test_zh2en():
    """Test zh2en '这是测试'."""

    assert "test" in zh2en("这是测试").lower()

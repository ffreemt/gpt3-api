"""Test assemble_prompt."""
from gpt3_api.gpt3_api import assemble_prompt


def test_assemble_prompt1():
    """Test prompt."""

    # ['', '', 'Human: ', 'AI:', '', 'Human: query', 'AI:']
    _ = assemble_prompt("query").splitlines()
    assert 'Human: query' in _


def test_assemble_prompt2():
    """Test prompt."""

    # ['', '', 'Human: ', 'AI:', '', 'Human: query', 'AI:']
    _ = assemble_prompt("query").splitlines()
    assert sum(map(lambda x: 'human' in x.lower(), _)) == 2
    assert sum(map(lambda x: 'ai' in x.lower(), _)) == 2

"""Test assemble_prompt."""
from gpt3_api.gpt3_api import assemble_prompt


def test_assemble_prompt1():
    """Test prompt."""

    # ['', '', 'Human: ', 'AI:', '', 'Human: query', 'AI:']
    _ = assemble_prompt("query").splitlines()
    assert "Human: query" in _


def test_assemble_prompt2():
    """Test prompt."""

    # ['', '', 'Human: ', 'AI:', '', 'Human: query', 'AI:']
    _ = assemble_prompt("query").splitlines()
    assert sum(map(lambda x: "human" in x.lower(), _)) == 2
    assert sum(map(lambda x: "ai" in x.lower(), _)) == 2


_ = """
examples = [("Test text", 'test')]
t = assemble_prompt('abc', prefixes=("Text: ", "This text is about: "), examples=examples)
print(t)

examples = [("Test text", 'test')]
t = assemble_prompt('abc', prefixes=("Text: ", "Keywords: "), examples=examples)
print(t)

t = assemble_prompt('abc', prefixes=("Text: ", "Keywords: "))
print(t)

prompt = assemble_prompt(query, prefixes=("Text: ", "Keywords: "))
print(prompt)

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
  engine="davinci",
  prompt="Text: 据公告介绍，徐宏于2018年7月加入阿里巴巴并由2019年7月起担任公司的副首席财务官。加入阿里巴巴前，徐宏于1996年加入普华永道会计师事务所，并曾担任合伙人11年。彼现为多家公司担任董事，其中包括于以下于香港联交所上市的公司担任非执行董事，分別为高鑫零售有限公司，联华超市股份有限公司以及红星美凯龙家居集团股份有限公司。\n\nKeywords: 上市公司,阿里巴巴集团,高鑫零售有限公司,联华超市股份有限公司,红星美凯龙家居集团股份有限公司",
  temperature=0.1,
  max_tokens=176,
  top_p=1,
  frequency_penalty=0.8,
  presence_penalty=0,
  stop=["\n"]
)

sentence-transformers/distiluse-base-multilingual-cased-v2

# """

"""Test clas_zs."""
from pathlib import Path
from random import choices, seed
from string import ascii_lowercase
from logzero import logger
from gpt3_api.clas_zs import clas_zs
from gpt3_api.gpt3_api import assemble_prompt


def test_clas_zs1():
    """Test clas_zs 1: tests/test_en.txt."""
    filename = "tests/test_en.txt"
    filepath = Path(filename)
    if not filepath.exists():
        logger.error("[%s] does not exist, period -- exiting...", filepath.absolute())
        raise SystemExit(1)
    try:
        _ = filepath.read_text(encoding="utf8")
    except Exception as exc:
        logger.error(exc)
        logger.info("Make sure the file is in utf8 format.")
        raise SystemExit(1)

    # remove blank lines
    paras = [elm.strip() for elm in _.splitlines() if elm.strip()]

    seed = 42
    len_ = len(paras)
    labels = ["".join(choices(ascii_lowercase, k=3)) for idx in range(len_)]

    examples = [*zip(paras, labels)]

    # prompt = assemble_prompt(examples[0][0], examples=examples, prefixes=("Text: ", "Category: "))

    res = []
    for elm in examples:
        _ = clas_zs(elm[0], examples)
        res.append((elm[1], _))
    assert sum(elm[0] == elm[1].strip() for elm in res) > 20


_ = '''
def test_clas_zs2():
    """Test clas_zs with tests/wu_ch3_en.txt.

    maximum context length is 2049 tokens

    6916 in your prompt, 32 for the completion
    """
    filename = "tests/wu_ch3_en.txt"
    filepath = Path(filename)
    if not filepath.exists():
        logger.error("[%s] does not exist, period -- exiting...", filepath.absolute())
        raise SystemExit(1)
    try:
        _ = filepath.read_text(encoding="utf8")
    except Exception as exc:
        logger.error(exc)
        logger.info("Make sure the file is in utf8 format.")
        raise SystemExit(1)

    # remove blank lines
    paras = [elm.strip() for elm in _.splitlines() if elm.strip()]

    seed = 42
    len_ = len(paras)
    labels = ["".join(choices(ascii_lowercase, k=3)) for idx in range(len_)]

    examples = [*zip(paras, labels)]

    # prompt = assemble_prompt(examples[0][0], examples=examples, prefixes=("Text: ", "Category: "))

    res = []
    for elm in examples:
        _ = clas_zs(elm[0], examples)
        res.append((elm[1], _))
    assert sum(elm[0] == elm[1].strip() for elm in res) > 20
# '''

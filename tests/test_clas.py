"""Test clas."""
from pathlib import Path
import re
from logzero import logger
from gpt3_api.clas import clas


def test_clas1():
    """Test clas with tests/test_en.txt."""
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
    _ = [elm.strip() for elm in _.splitlines() if elm.strip()]
    examples = [(elm, str(idx)) for idx, elm in enumerate(_)]

    assert clas(examples[0][0], examples) == examples[0][1]

    # 22/33 25/33 = ~75%, 11s, 1/3 per classification
    assert (
        sum(clas(elm[0], examples) == elm[1] for elm in examples) > len(examples) // 2
    )


_ = r'''
def test_clas_wuch3():
    """Test clas with tests/wu_ch3_en.txt."""
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
    _ = [elm.strip() for elm in _.splitlines() if elm.strip()]
    len_ = len(_)

    # labels = [" ".join([f"{idx:03}"] * 3) for idx in range(len_)]

    labels = [[f"{idx:03}"] + re.sub(r"[^ \w*-]", "", elm).lower().split()[:1] for idx, elm in enumerate(_)]
    labels = ["".join(elm) for elm in labels]

    labels = [f"{elm:03}" for elm in range(len_)]

    examples = [*zip(_, labels)]

    vals = [(clas(elm[0], examples), elm[1]) for elm in examples]

    # [str(elm) for elm in range(len_)]: 11/len_
    len([elm for elm in vals if elm[0] == elm[1]]) / len_


# '''

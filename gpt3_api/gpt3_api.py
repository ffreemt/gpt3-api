"""Define gpt3_api: wrap openai.Completion.create.

set OPENAI_API_KEY=your_openai_key
curl -H "Authorization: Bearer %OPENAI_API_KEY%" https://api.openai.com/v1/engines
# linux and friends:
# export OPENAI_API_KEY=your_openai_key
# curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/engines

"""
# pylint: disable=too-many-arguments, too-many-locals

from typing import List, Optional, Tuple

from collections import deque
from itertools import chain
import logzero
from logzero import logger
import openai

from .config import Settings
config = Settings()
openai.api_key = config.api_key

logzero.loglevel(10)


# fmt: off
def get_resp(
        prompt: str,
        engine: str = "davinci",
        temperature: float = 0.9,
        max_tokens: int = 150,
        top_p: int = 1,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.6,
        stop: Tuple[str, str, str, str] = (" Human:", "\n", " AI:", "\n\n"),
        **kwargs,
) -> str:
    # fmt: on
    """Get response from openai."""
    try:
        response = openai.Completion.create(
            prompt=prompt,
            engine=engine,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop=stop,
            **kwargs,
        )
        logger.debug(response)
    except Exception as exc:
        logger.error(exc)
        return str(exc)

    try:
        resp = response.choices[0].text
    except Exception as exc:
        logger.error(exc)
        resp = str(exc)

    return resp


# fmt: off
def gpt3_api(
        query: str,
        prompt: str = "",
        engine: str = "davinci",  # davinci, curie, babbage, ada
        # prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: I'd like to cancel my subscription.\nAI:",  # pylint: disable=line-too-long
        temperature: float = 0.9,
        max_tokens: int = 150,
        top_p: int = 1,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.6,
        # stop: List[str] = ["\n", " Human:", " AI:"],
        stop: Tuple[str, str, str, str] = (" Human:", "\n", " AI:", "\n\n"),
        prime_on: bool = False,
        # reprime: bool = False,
        preamble: str = "",
        examples: Optional[List[Tuple[str, str]]] = None,
        deq_len: int = 100,
        # proxy: str = None,
        # proxy: Optional[str] = None,
        **kwargs,
) -> str:
    # fmt: on
    """Define api.

    Args:
        stop: prefix0, suffix0, prefix1 suffix1
            to form the prompt
            preamble + suffix1 + prefix0 + query + suffix0 + prefix1 + result + suffix1 + prefix0 + query + suffix0 + prefix1
        preamble: use when priming
        examples: list of (query, result) pairs
        deq_len: queue length

        openai.completion args: check [openai docs](https://beta.openai.com/docs/api-reference/completions/create)
        engine: https://beta.openai.com/docs/engines
        temperature:

    Returns:
        response = openai.Completion()
        response.choices[0].text
    """
    prefix0, suffix0, prefix1, suffix1 = stop
    # may use your own prompt any time
    if prompt:
        return get_resp(
            prompt=prompt,
            engine=engine,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop=stop,
            **kwargs,
        )

    # initialize deq and store examples and history as function attribute.
    try:
        # only run on first call
        _ = gpt3_api.deq
        preamble_ = ""
    except AttributeError:
        preamble_ = preamble
        if examples is not None:
            gpt3_api.deq = deque(chain.from_iterable(examples), deq_len)
        else:
            gpt3_api.deq = deque([], deq_len)

    # re-prime when needed
    if prime_on:
        # construct prompt when not provided by user,
        if not prompt:
            # examples is not None needed for type hint
            if not examples and examples is not None:
                _ = chain.from_iterable(examples)  # original prime data
            else:
                _ = ""
            _ = f"{suffix0}{prefix1}".join(_)
            prompt = f"{preamble}{prefix0}{_}{suffix1}"
            prompt += f"{prefix0}{query}{suffix0}{prefix1}"
    else:  # normal op
        _ = f"{suffix0}{prefix1}".join(gpt3_api.deq)
        prompt = f"{preamble_}{prefix0}{_}{suffix1}"
        prompt += f"{prefix0}{query}{suffix0}{prefix1}"

    resp = get_resp(
        prompt=prompt,
        engine=engine,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop,
        **kwargs,
    )

    # update deq if resp is not empty
    if not resp.strip():
        gpt3_api.deq.append(query)
        gpt3_api.deq.append(resp)

    return resp


def main():
    """Run some test codes."""
    # preamble = "Tell a joke."
    preamble = "Translatiton"
    # preamble = ""

    temperature = 0.5
    frequency_penalty = 0
    presence_penalty = 0

    examples = [
        ("Good solution by Vengat, and this also works with rjust.", "Vengat 提供了很好的解决方案，这也适用于 rjust。"),
        # ("Good morning", "早上好"),
        # ("I love you", "我爱你"),
        ("I have tried to use all GPT-3 engines to reach the results and the only that gives back an accurate result is DAVINCI.", "我尝试使用所有 GPT-3 引擎来获得结果，唯一能返回准确结果的是 DAVINCI。")
    ]
    stop = ("English:", "\n", "中文:", "\n###\n")
    # stop = ("English:", "\n", "中文:", "\n***\n")
    # stop = ("English:", "\n", "中文:", "\n")

    # "Hi there!",
    "I hate you!",
    # "Good morning",
    # "Good solution by Vengat, and this also works with rjust.",
    query = "What's your name?",
    # query = "I have tried to use all GPT-3 engines to reach the results and the only that gives back an accurate result is DAVINCI.",

    while True:
        query = "Make sure you have a valid API Token to use GPT-3."
        query = input("English: ")
        if query.strip().lower()[:4] in ["quit", "exit", "stop"]:
            break

        _ = gpt3_api(
            query,
            preamble=preamble,
            stop=stop,
            temperature=temperature,
            frequency_penalty = frequency_penalty,
            presence_penalty = presence_penalty,
        )
        print("中文： ", _)


if __name__ == "__main__":
    main()

"""Test get_resp."""
from gpt3_api.gpt3_api import assemble_prompt, get_resp


def test_get_resp0():
    """Test get_resp."""
    query = "test"
    query = "what is your name"
    query = "do you have a girl friend"
    suffixes = ("\n", "\n###\n")
    suffixes = ("\n", "\n\n")
    prompt = assemble_prompt(
        query,
        preamble="chat",
        examples=[
            ("hi", "hi yourself"),
            ("having fun?", "yeah, you?"),
        ],
        # suffixes=suffixes,
    )
    resp = get_resp(
        prompt,
        temperature=0.245,
        # stop=suffixes[1]
        stop="\n\n",
    )
    print(resp)


def test_get_resp():
    """Test get_resp."""
    examples = [
        (
            "Good solution by Vengat, and this also works with rjust.",
            "Vengat 提供了很好的解决方案，这也适用于 rjust。",
        ),
        # ("Good morning", "早上好"),
        # ("I love you", "我爱你"),
        (
            "I have tried to use all GPT-3 engines to reach the results and the only that gives back an accurate result is DAVINCI.",
            "我尝试使用所有 GPT-3 引擎来获得结果，唯一能返回准确结果的是 DAVINCI。",
        ),
    ]

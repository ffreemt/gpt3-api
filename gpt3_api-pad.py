preamble = "Translatiton"
prefixes = ("English: ", "中文: ")
suffixes = ("\n", "\n\n")

engine: str = "davinci"
temperature: float = 0.2
max_tokens: int = 150
top_p: int = 1
frequency_penalty: float = 0.0  # -2..2, postive penalty
presence_penalty: float = 0.0
stop = None
stop = suffixes[1]

query1 = "What's your name?" 
examples1 = [
    ("hi", "hi yourself"),
]
_ = assemble_prompt(
    query1, 
    preamble="Chat",
    examples=examples1,
)
print(_)

response = openai.Completion.create(
    prompt=_,
    engine=engine,
    temperature=temperature,
    max_tokens=max_tokens,
    top_p=top_p,
    frequency_penalty=frequency_penalty,  # -2.0 and 2.0. Positive values penalize new tokens
    presence_penalty=presence_penalty,
    echo=echo,
    stop=stop,   # default to null
    # **kwargs,
)
logger.debug(response)

response.choices[0].get("text")
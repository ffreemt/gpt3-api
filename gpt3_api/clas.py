"""Classify texts to multiple classes.

https://beta.openai.com/docs/api-reference/searches 200 labels
https://beta.openai.com/docs/guides/classifications
Up to 200 labeled examples

---
nlpcloud 0-201
https://nlpcloud.io/home/playground/classification
John Doe is a Go Developer at Google. He has been working there for 10 years and has been awarded employee of the year.

english bart-large-mnli
multiligual xml-roberta-large-xnli

bart
10	0.8118433952331543
1	0.5012564659118652
156	0.47537827491760254
4	0.4386976361274719
2	0.43474289774894714
152	0.4264623522758484

roberta
161	0.3706091344356537
168	0.3546360433101654
152	0.3349819481372833
158	0.3317909240722656
171	0.3146763741970062
131	0.3106502890586853
172	0.3091292083263397
162	0.3048304319381714


John Doe 是 Google 的 Go 开发人员。 他已经在那里工作了 10 年，并被授予年度员工奖。
bad gateway

roberta
10	0.678921639919281
161	0.5564551949501038
131	0.5222370028495789
201	0.5204747319221497
171	0.520220160484314
162	0.5155285000801086
172	0.49987271428108215

# ---
# https://beta.openai.com/examples/default-classification

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = '''The following is a list of companies and the categories they fall into\n\nFacebook: Social media, Technology\nLinkedIn: Social media, Technology, Enterprise, Careers\nUber: Transportation, Technology, Marketplace\nUnilever: Conglomerate, Consumer Goods\nMcdonalds: Food, Fast Food, Logistics, Restaurants\nFedEx:"'''

prompt = '''The following is a list of keywords and their category labels
Social media, Technology: zero
Social media, Technology, Enterprise, Careers: one
Conglomerate, Consumer Goods: three
Transportation, Technology, Marketplace: two
Food, Fast Food, Logistics, Restaurants: four
Logistics, Transportation: five
Food, Fast Food, Logistics, Restaurants: four
Food, Fast Food, Logistics, Restaurants: '''

# response =
openai.Completion.create(
  engine="davinci",
  prompt=prompt,
  temperature=0,
  max_tokens=6,
  top_p=1.0,
  # top_p=.9,
  frequency_penalty=0.0,
  presence_penalty=0.0,
  stop=["\n"]
)

import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

openai.Classification.create(
  search_model="ada",
  model="curie",
  examples=[
    # ["A happy moment", "Positive"],
    # ["I am sad.", "Negative"],
    # ["I am feeling awesome", "Positive"]
    ("Social media, Technology", '0'),
    ("Social media, Technology, Enterprise, Careers", '1'),
    ("Conglomerate, Consumer Goods", '2'),
    ("Transportation, Technology, Marketplace", '3'),
    ("Food, Fast Food, Logistics, Restaurants", '4'),
    ("Logistics, Transportation", '5'),
    ("Food, Fast Food, Logistics, Restaurants", '4'),
  ],
  # query="It is a raining day :(",
  # labels=["Positive", "Negative", "Neutral"],

  # query = "Consumer Goods, Social media",
  # query = "Food, Fast Food, Logistics, Restaurants The following",
  query = "Transportation, Technology",  # 3
  labels=[str(elm) for elm in [0, 1, 2, 3, 4, 5]],
)


# """

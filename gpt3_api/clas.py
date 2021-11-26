"""Classify texts to multiple classes.

https://beta.openai.com/docs/api-reference/searches 200 labels

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

"""
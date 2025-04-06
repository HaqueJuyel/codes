from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")

text = "I love using transformers for NLP tasks!"

result = sentiment_pipeline(text)
print(result) 
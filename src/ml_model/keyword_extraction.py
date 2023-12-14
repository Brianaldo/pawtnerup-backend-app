# from keybert import KeyBERT

# model = KeyBERT('distilbert-base-nli-mean-tokens')


# class KeywordExtraction:
#     def __init__(self):
#         self.model = model

#     def extract(self, text: str) -> list[str]:
#         keywords_with_scores = self.model.extract_keywords(
#             text, keyphrase_ngram_range=(1, 1), stop_words='english', top_n=3
#         )
#         keywords = [keyword for keyword, _ in keywords_with_scores]

#         return keywords

import requests


class KeywordExtraction:
    def __init__(self):
        self.url = "http://10.184.0.3:5000"

    def extract(self, text: str) -> list[str]:
        files = {
            'text': (None, text),
        }

        response = requests.post(
            '{}/extract'.format(self.url), files=files
        )
        return response.json()['keywords']

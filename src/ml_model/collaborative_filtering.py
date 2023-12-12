import pandas as pd
from pydantic import BaseModel
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

from pet.model import AgeEnum, GenderEnum


history_df = pd.read_csv(
    os.getcwd() + '/dataset/Adopter History (Processed).csv')


class InputAdopter(BaseModel):
    gender: list[GenderEnum]
    age: list[AgeEnum]
    breed: list[str]


class MostSimilarAdopter(BaseModel):
    breed: str
    age: AgeEnum
    gender: GenderEnum


class CollaborativeFilteringModel:
    def __init__(self):
        self.history_df = history_df

    def get_most_similar(self, adopter: InputAdopter) -> MostSimilarAdopter:
        adopter.gender = list(map(lambda el: el.to_str(), adopter.gender))
        adopter.age = list(map(lambda el: el.to_str(), adopter.age))

        adopter.gender = [', '.join(adopter.gender)]
        adopter.age = [', '.join(adopter.age)]
        adopter.breed = [', '.join(adopter.breed)]

        adopter_df = pd.DataFrame.from_dict(
            adopter.model_dump())

        adopter_df['combined_preferences'] = adopter_df[[
            'gender', 'age', 'breed']
        ].agg(' '.join, axis=1)

        vectorizer = CountVectorizer().fit(
            history_df['combined_preferences']._append(adopter_df['combined_preferences']))
        history_vectors = vectorizer.transform(
            history_df['combined_preferences'])
        adopters_vectors = vectorizer.transform(
            adopter_df['combined_preferences'])

        similarity_scores = cosine_similarity(
            adopters_vectors[0], history_vectors)[0]
        ranked_users = np.argsort(similarity_scores)[::-1]

        highest_ranked_index = ranked_users[0]
        highest_ranked_user = history_df.iloc[highest_ranked_index]

        return MostSimilarAdopter(
            breed=highest_ranked_user['Adopted Dog\'s Breed/Sub-breed'],
            age=AgeEnum.from_str(highest_ranked_user['Adopted Dog\'s Age']),
            gender=GenderEnum.from_str(
                highest_ranked_user['Adopted Dog\'s Gender'])
        )

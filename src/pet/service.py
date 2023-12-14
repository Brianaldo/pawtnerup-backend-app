from datetime import date
from typing import Union
from _common.exceptions import NotFoundException
from _infrastructure.database.exceptions import NotFoundError
from _infrastructure.object_storage.client import ObjectStorageClient
from pet.model import Pet, PetMediaRequestBody, PetMediaTypeRequest, PetTyped
from pet.repository import PetRepository
import datetime

from shelter.repository import ShelterRepository


class PetService:
    def __init__(self):
        self.pet_repo = PetRepository()
        self.shelter_repo = ShelterRepository()
        self.storage_client = ObjectStorageClient()
        from ml_model.keyword_extraction import KeywordExtraction
        self.keyword_model = KeywordExtraction()

    def create_pet(self, estimate_age: float, shelter_email: str, **kwargs: PetTyped) -> tuple[Pet, list[str]]:
        estimate_born_date = datetime.datetime.now(
        ) - datetime.timedelta(days=(estimate_age*365.24))

        post_media_urls: list[str] = []
        for i in range(len(kwargs.get('media'))):
            ext = kwargs.get('media')[i].split('.')[-1]
            new_filename, url = self.storage_client.post_presigned_url(
                ext
            )
            post_media_urls.append(url)
            kwargs.get('media')[i] = new_filename

        labels = self.keyword_model.extract(kwargs.get('rescue_story'))

        return (self.pet_repo.create(shelter_email=shelter_email, born_date=estimate_born_date, labels=labels, **kwargs).to_model(), post_media_urls)

    def get_pet_by_shelter(self, shelter_email: str) -> list[Pet]:
        pets = self.pet_repo.fetch_by_shelter(shelter_email=shelter_email)
        return [pet.to_model() for pet in pets]

    def get_pet(self, shelter_email: str, pet_id: int) -> Pet:
        shelter = self.shelter_repo.get_one_by_filter(
            email=shelter_email
        )
        pet = self.pet_repo.get_one_by_filter(
            shelter_id=shelter.id,
            id=pet_id
        )

        return pet.to_model()

    def update_pet(self, shelter_email: str, pet_id: int, estimate_age: float, **kwargs: PetTyped) -> Pet:
        try:
            estimate_born_date = datetime.datetime.now(
            ) - datetime.timedelta(days=(estimate_age*365.24))

            labels = self.keyword_model.extract(kwargs.get('rescue_story'))
            print(labels)

            pet = self.pet_repo.update(
                pet_id=pet_id,
                shelter_email=shelter_email,
                born_date=estimate_born_date,
                labels=labels,
                **kwargs
            )

            return pet.to_model()
        except NotFoundError:
            raise NotFoundException("Shelter or pet not found")
        except Exception as e:
            print(e)
            raise e

    def update_media(self, shelter_email: str, pet_id: int, media: list[PetMediaRequestBody]) -> tuple[Pet, list[str]]:
        try:
            shelter = self.shelter_repo.get_one_by_filter(
                email=shelter_email
            )
            pet = self.pet_repo.get_one_by_filter(
                shelter_id=shelter.id,
                id=pet_id
            )

            filename_req = [media[i].filename for i in range(
                len(media)) if media[i].type != PetMediaTypeRequest.ADD
            ]
            for i in range(len(pet.media)):
                if pet.media[i] not in filename_req:
                    raise ValueError(
                        f"Media {pet.media[i]} not found in request"
                    )

            for i in range(len(filename_req)):
                if filename_req[i] not in pet.media:
                    raise ValueError(
                        f"Media {filename_req[i]} not found in database"
                    )

            media_urls: list[Union[str, None]] = []
            new_media: list[str] = []
            for i in range(len(media)):
                if media[i].type == PetMediaTypeRequest.DELETE:
                    self.storage_client.delete_file(media[i].filename)
                    media_urls.append(None)
                elif media[i].type == PetMediaTypeRequest.ADD:
                    ext = media[i].filename.split('.')[-1]
                    new_filename, url = self.storage_client.post_presigned_url(
                        ext
                    )
                    media_urls.append(url)
                    new_media.append(new_filename)
                elif media[i].type == PetMediaTypeRequest.UPDATE:
                    for j in range(len(pet.media)):
                        if pet.media[j] == media[i].filename:
                            url = self.storage_client.put_presigned_url(
                                media[i].filename
                            )
                            media_urls.append(url)
                            new_media.append(media[i].filename)
                            break
                else:
                    new_media.append(media[i].filename)
                    media_urls.append(None)

            pet.media = new_media
            self.pet_repo.update(
                pet_id=pet.id,
                shelter_email=shelter_email,
                **pet.to_model().model_dump()
            )

            return (pet.to_model(), media_urls)
        except ValueError as e:
            raise ValueError(e or "Media not found")
        except NotFoundError as e:
            raise NotFoundException(e or "Shelter or pet not found")
        except Exception as e:
            print(e)
            raise e

    def delete_pet(self, shelter_email: str, pet_id: int) -> int:
        try:
            shelter = self.shelter_repo.get_one_by_filter(
                email=shelter_email
            )
            pet = self.pet_repo.get_one_by_filter(
                shelter_id=shelter.id,
                id=pet_id
            )

            for i in range(len(pet.media)):
                try:
                    self.storage_client.delete_file(pet.media[i])
                except Exception as e:
                    print(e)

            self.pet_repo.delete(
                id=pet.id
            )

            return pet.id
        except NotFoundError:
            raise NotFoundException("Shelter or pet not found")
        except Exception as e:
            print(e)
            raise e

import datetime

from django.db.models import QuerySet
from django.http import QueryDict
from rest_framework import exceptions

from movie.models import Person, Movie, PersonRoleInMovie


class PersonService:

    @staticmethod
    def get_all_persons(request_params: QueryDict) -> QuerySet[Person]:

        persons = Person.objects.prefetch_related('movies')

        return persons

    @staticmethod
    def delete_person_by_id(*, person_id: int) -> None:

        try:
            person = Person.objects.get(pk=person_id)
        except Person.DoesNotExist as e:
            raise exceptions.NotFound(
                detail=f"The person with ID-{person_id} is not found in the list."
            )

        person.delete()

    @staticmethod
    def update_person_by_id(*,
                            person_id: int,
                            data: dict
    ) -> Person:

        try:
            person = Person.objects.get(pk=person_id)
        except Person.DoesNotExist as e:
            raise exceptions.NotFound(
                detail=f"The person with ID-{person_id} is not found in the list."
            )

        if data.get("name"):
            person.name = data.get("name")
        if data.get("birth_date"):
            person.birth_date = data.get("birth_date")
        if data.get("biography"):
            person.biography = data.get("biography")

        person.save()

        return person

    @staticmethod
    def create_person(*,
                      name: str,
                      birth_date: datetime,
                      biography: str,
                      role: str,
                      movie_id: int
    ) -> Person:

        person = Person.objects.get_or_create(
                name=name,
                birth_date=birth_date,
                biography=biography
        )

        movie = Movie.objects.get(id=movie_id)

        person_role = PersonRoleInMovie(
            movie=movie,
            person=person[0],
            role=role
        )
        person_role.save()

        return person[0]

    @staticmethod
    def get_person_by_id(person_id: int) -> Person:

        try:
            person = Person.objects.prefetch_related('movies').get(pk=person_id)
        except Person.DoesNotExist as e:
            raise exceptions.NotFound(
                detail=f"The person with ID-{person_id} has not been found."
            )

        return person



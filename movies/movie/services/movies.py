from django.db import IntegrityError
from django.db.models import QuerySet, Q
from django.http import QueryDict
from rest_framework import exceptions

from movie.common.utils import DataTransformation
from movie.filters import MovieFilter
from movie.models import Movie, Genre, MovieGenre, Person, PersonRoleInMovie


class MovieService:

    @staticmethod
    def create_movie(data: dict) -> Movie:

        try:
            movie = Movie(
                title=data.get('title'),
                year=int(data.get('year')),
                released=data.get('released'),
                runtime=data.get('runtime'),
                awards=data.get('awards'),
                poster=data.get('poster'),
                language=data.get('language'),
                country=data.get('country'),
                plot=data.get('plot'),
                imdbRating=data.get('imdbRating')
            )
            movie.save()
        except IntegrityError as e:
            raise exceptions.PermissionDenied(
                detail="You trying to add a movie that is already in the collection"
            )

        trans = DataTransformation()
        genres = trans.get_values(data.get('genre'))
        actors = trans.get_values(data.get('actor'))
        directors = trans.get_values(data.get('director'))
        writers = trans.get_values(data.get('writer'))

        for g in genres:

            genre = Genre.objects.get_or_create(genre = g)

            movie_genre = MovieGenre(
                movie=movie,
                genre=genre[0]
            )
            movie_genre.save()

        for a in actors:

            person = Person.objects.get_or_create(name=a)

            person_role = PersonRoleInMovie(
                movie=movie,
                person=person[0],
                role='actor'
            )
            person_role.save()

        for a in writers:

            person = Person.objects.get_or_create(name=a)

            person_role = PersonRoleInMovie(
                movie=movie,
                person=person[0],
                role='writer'
            )
            person_role.save()

        for a in directors:

            person = Person.objects.get_or_create(name=a)

            person_role = PersonRoleInMovie(
                movie=movie,
                person=person[0],
                role='director'
            )
            person_role.save()

        return movie

    @staticmethod
    def delete_movie_by_id(*, movie_id: int) -> None:

        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist as e:
            raise exceptions.NotFound(
                detail=f"The movie with ID-{movie_id} is not found in the movie list."
            )

        movie.delete()

    @staticmethod
    def update_movie_by_id(*,
                           movie_id: int,
                           data: dict
    ) -> Movie:

        try:
            movie = Movie.objects.prefetch_related('genres', 'person_roles', 'persons').get(pk=movie_id)
        except Movie.DoesNotExist as e:
            raise exceptions.NotFound(
                detail=f"The movie with ID-{movie_id} is not found in the movie list."
            )

        if data.get("title"):
            movie.title = data.get("title")
        if data.get("year"):
            movie.year = data.get("year")
        if data.get("released"):
            movie.released = data.get("released")
        if data.get("runtime"):
            movie.runtime = data.get("runtime")
        if data.get("awards"):
            movie.runtime = data.get("awards")
        if data.get("poster"):
            movie.poster = data.get("poster")
        if data.get("language"):
            movie.language = data.get("language")
        if data.get("country"):
            movie.country = data.get("country")
        if data.get("plot"):
            movie.plot = data.get("plot")

        if data.get("genre"):
            try:
                genre = Genre.objects.get(genre=data.get("genre"))
            except Genre.DoesNotExist as e:
                genre = Genre(genre=data.get("genre"))
                genre.save()

            try:
                movie_genre = MovieGenre.objects.get(movie=movie, genre=genre)
                movie_genre.delete()
            except MovieGenre.DoesNotExist as e:
                movie_genre = MovieGenre(
                    movie=movie,
                    genre=genre
                )
                movie_genre.save()

        if data.get("actor"):
            try:
                person = Person.objects.get(name=data.get("actor"))
            except Person.DoesNotExist as e:
                person = Person(name=data.get("actor"))
                person.save()

            try:
                person_role = PersonRoleInMovie.objects.get(movie=movie, person=person, role="actor")
                person_role.delete()
            except PersonRoleInMovie.DoesNotExist as e:
                person_role = PersonRoleInMovie(
                    movie=movie,
                    person=person,
                    role="actor"
                )
                person_role.save()

        if data.get("writer"):
            try:
                person = Person.objects.get(name=data.get("writer"))
            except Person.DoesNotExist as e:
                person = Person(name=data.get("writer"))
                person.save()

            try:
                person_role = PersonRoleInMovie.objects.get(movie=movie, person=person, role="writer")
                person_role.delete()
            except PersonRoleInMovie.DoesNotExist as e:
                person_role = PersonRoleInMovie(
                    movie=movie,
                    person=person,
                    role="writer"
                )
                person_role.save()

        if data.get("director"):
            try:
                person = Person.objects.get(name=data.get("director"))
            except Person.DoesNotExist as e:
                person = Person(name=data.get("director"))
                person.save()

            try:
                person_role = PersonRoleInMovie.objects.get(movie=movie, person=person, role="director")
                person_role.delete()
            except PersonRoleInMovie.DoesNotExist as e:
                person_role = PersonRoleInMovie(
                    movie=movie,
                    person=person,
                    role="director"
                )
                person_role.save()

        movie.save()

        return movie

    @staticmethod
    def get_all_movies(request_params: QueryDict) -> QuerySet:

        movies = Movie.objects.prefetch_related('genres', 'person_roles', 'persons')

        if request_params:
            movies = MovieFilter(request_params, movies).qs

        search_text = request_params.get('search', None)
        if search_text:
            movies = movies.filter(
                Q(title__icontains=search_text) |
                Q(year__icontains=search_text) |
                Q(plot__icontains=search_text)
            )

        ordering = request_params.get('ordering', '-created_at')
        if ordering:
            movies = movies.order_by(ordering)

        return movies.distinct()

    @staticmethod
    def get_movie_by_id(movie_id: int) -> Movie:

        try:
            movie = Movie.objects.prefetch_related('genres', 'person_roles', 'comments').get(id=movie_id)
        except Movie.DoesNotExist as e:
            raise exceptions.NotFound(
                detail=f"The movie with ID-{movie_id} has not been found."
            )

        return movie



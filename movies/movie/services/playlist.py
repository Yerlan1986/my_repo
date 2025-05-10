from django.db import IntegrityError
from django.db.models import QuerySet
from requests import Request
from rest_framework import exceptions

from movie.models import Movie, UserPlayList, Comment, MovieGenre, Recommendation


class PlaylistService:

    @staticmethod
    def add_movie_by_id(user, movie_id: int) -> UserPlayList:

        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist as e1:
            raise exceptions.NotFound(
                detail=f"The movie with ID-{movie_id} is not found in the movie list."
            )

        try:
            playlist = UserPlayList(
                user=user,
                movie=movie
            )
            playlist.save()
        except IntegrityError as e2:
            raise exceptions.PermissionDenied(
                detail="you trying to add a movie that is already in the collection"
            )

        return playlist

    @staticmethod
    def delete_movie_from_playlist_by_id(*, user, movie_id: int) -> None:

        try:
            entry = UserPlayList.objects.get(user=user, movie_id=movie_id)
        except UserPlayList.DoesNotExist as e:
            raise exceptions.NotFound(
                detail=f"The movie with ID-{movie_id} is not found in the playlist."
            )

        if entry.user.id != user.id:
            raise exceptions.PermissionDenied(
                detail="You can update only your comments!"
            )
        entry.delete()

    @staticmethod
    def show_all(request: Request) -> QuerySet[UserPlayList]:

        playlist = UserPlayList.objects.filter(user=request.user)

        return playlist

    @staticmethod
    def get_recommendations(*, user_id: int) -> QuerySet:

        genres_id = list(
            Recommendation.objects
            .filter(user=user_id)
            .order_by('-count')
            .values_list('genre', flat=True)[:2]
        )

        rated_movie_id = list(
            Comment.objects
            .filter(user=user_id)
            .values_list('movie_id', flat=True)
        )

        playlist_movie_id = list(
            UserPlayList.objects
            .filter(user=user_id)
            .values_list('movie_id', flat=True)
        )

        if genres_id:
            movies_id = list(
                MovieGenre.objects
                .filter(genre_id__in=genres_id)
                .values_list('movie_id', flat=True)
            )

            movies = (
                Movie.objects
                .filter(pk__in=movies_id)
                .exclude(pk__in=rated_movie_id)
                .exclude(pk__in=playlist_movie_id)
                .order_by('-imdbRating', '-average_rating', '-year')[:3]
            )
        else:
            movies = (
                Movie.objects
                .exclude(pk__in=rated_movie_id)
                .exclude(pk__in=playlist_movie_id)
                .order_by('-imdbRating', '-average_rating', '-year')[:3]
            )

        return movies








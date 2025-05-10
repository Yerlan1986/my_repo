
from django.db import IntegrityError
from django.db.models import QuerySet, F
from django.http import QueryDict
from rest_framework import exceptions
from django.db.models import Avg


from authorization.models import User
from movie.models import Person, Movie, Comment, MovieGenre, Recommendation


class CommentService:

    @staticmethod
    def create_comment(*,
                      text: str,
                      rating: int,
                      movie_id: int,
                      author: User
    ) -> Comment:

        try:
            comment, created = Comment.objects.get_or_create(
                text=text,
                rating=rating,
                movie_id=movie_id,
                user=author
            )

            if not created:
                raise exceptions.PermissionDenied(
                    detail=f"You already commented on the film with ID -{movie_id}"
                )

            comment.save()

        except IntegrityError as e:
            raise exceptions.PermissionDenied(
                detail=f"The movie with ID-{movie_id} is not found in the movie list."
            )

        average_rating = (Comment
                            .objects
                              .filter(movie_id=movie_id)
                              .aggregate(average_rating=Avg("rating"))
                              )

        Movie.objects.filter(id=comment.movie.id).update(average_rating=average_rating['average_rating'])
        genres = MovieGenre.objects.filter(movie=comment.movie.id)

        if rating in (4, 5):
            for g in genres:

                recommendation, created = (Recommendation
                                            .objects
                                            .get_or_create(
                                                    user=author,
                                                    genre=g.genre
                                                    )
                                            )
                if not created:
                        (Recommendation.
                         objects
                         .filter(pk=recommendation.pk)
                         .update(count=F('count') + 1)
                         )

        return comment

    @staticmethod
    def delete_comment_by_id(*, comment_id: int, author_id: int) -> None:

        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist as e:
            raise exceptions.NotFound(
                detail=f"The comment with ID-{comment_id} is not found in the comments."
            )

        if comment.user.id != author_id:
            raise exceptions.PermissionDenied(
                detail="You can delete only your comments!"
            )

        movie_id = comment.movie.id

        comment.delete()

        average_rating = (Comment
                            .objects
                              .filter(movie_id=movie_id)
                              .aggregate(average_rating=Avg("rating"))
                              )
        Movie.objects.filter(id=comment.movie.id).update(average_rating=average_rating['average_rating'])

    @staticmethod
    def update_comment_by_id(*,
                            comment_id: int,
                            data: dict,
                            author_id: int
    ) -> Comment:

        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist as e:
            raise exceptions.NotFound(
                detail=f"The comment with ID-{comment_id} is not found in the comments."
            )

        if comment.user.id != author_id:
            raise exceptions.PermissionDenied(
                detail="You can update only your comments!"
            )

        if data.get("text"):
            comment.text = data.get("text")
        if data.get("rating"):
            comment.rating = data.get("rating")

        movie_id = comment.movie.id

        comment.save()

        average_rating = (Comment
                            .objects
                              .filter(movie_id=movie_id)
                              .aggregate(average_rating=Avg("rating"))
                              )
        Movie.objects.filter(id=comment.movie.id).update(average_rating=average_rating['average_rating'])

        return comment

    @staticmethod
    def get_all_comments(request_params: QueryDict, movie_id: int) -> QuerySet[Person]:

        comments = Comment.objects.prefetch_related('movie').filter(movie=movie_id)

        return comments
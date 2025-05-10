from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.request import Request

from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from movie.common.utils import inline_serializer, DataTransformation
from movie.services.movies import MovieService

from movie.movie_data import pars


class MovieCreateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=250)
        year = serializers.IntegerField()
        released = serializers.CharField(max_length=250)
        runtime = serializers.CharField(max_length=250)
        awards = serializers.CharField(max_length=250)
        poster = serializers.CharField(max_length=250)
        language = serializers.CharField(max_length=250)
        country = serializers.CharField(max_length=250)
        genre = serializers.CharField(max_length=250)
        plot = serializers.CharField()
        director = serializers.CharField(max_length=250)
        writer = serializers.CharField(max_length=250)
        actor = serializers.CharField(max_length=250)
        average_rating = serializers.FloatField(required=False)
        imdbRating = serializers.FloatField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField(max_length=250)
        year = serializers.IntegerField()
        released = serializers.CharField(max_length=250)
        runtime = serializers.CharField(max_length=250)
        awards = serializers.CharField(max_length=250)
        poster = serializers.CharField(max_length=250)
        language = serializers.CharField(max_length=250)
        country = serializers.CharField(max_length=250)
        average_rating = serializers.FloatField()
        imdbRating = serializers.FloatField()

        plot = serializers.CharField()

        genres = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "genre": serializers.CharField(max_length=250)
            }
        )

        person_roles = inline_serializer(
            many=True,
            fields={
                "person": inline_serializer(
                    fields={
                        "id": serializers.IntegerField(),
                        "name": serializers.CharField()
                    }
                ),
                "role": serializers.CharField()
            }
        )

    def post(self, request:Request) -> Response:

        movie_data = pars.get_movie(request.data.get('title'))
        transform = DataTransformation()

        movie_data = transform.transformation(movie_data)

        data = self.InputSerializer(data=movie_data)
        data.is_valid(raise_exception=True)

        movie_service = MovieService()
        movie = movie_service.create_movie(
            data.validated_data
        )

        return Response(
            data=self.OutputSerializer(movie).data,
            status=status.HTTP_201_CREATED
        )


class MovieDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def delete(self, request: Request, movie_id: int) -> Response:

        movie_service = MovieService()

        movie_service.delete_movie_by_id(movie_id=movie_id)

        return Response(
            data={
                "detail": f"The movie with ID-{movie_id} "
                          f"has been successfully deleted from the movie list"
            },
            status=status.HTTP_200_OK
        )


class MovieUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=250, required=False)
        year = serializers.IntegerField(required=False)
        released = serializers.CharField(max_length=250, required=False)
        runtime = serializers.CharField(max_length=250, required=False)
        awards = serializers.CharField(max_length=250, required=False)
        poster = serializers.CharField(max_length=250, required=False)
        language = serializers.CharField(max_length=250, required=False)
        country = serializers.CharField(max_length=250, required=False)
        genre = serializers.CharField(max_length=250, required=False)
        plot = serializers.CharField(required=False)
        director = serializers.CharField(max_length=250, required=False)
        writer = serializers.CharField(max_length=250, required=False)
        actor = serializers.CharField(max_length=250, required=False)
        director = serializers.CharField(max_length=250, required=False)
        writer = serializers.CharField(max_length=250, required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField(max_length=250)
        year = serializers.IntegerField()
        released = serializers.CharField(max_length=250)
        runtime = serializers.CharField(max_length=250)
        awards = serializers.CharField(max_length=250)
        poster = serializers.CharField(max_length=250)
        language = serializers.CharField(max_length=250)
        country = serializers.CharField(max_length=250)
        average_rating = serializers.FloatField()
        imdbRating = serializers.FloatField()

        plot = serializers.CharField()

        genres = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "genre": serializers.CharField(max_length=250)
            }
        )

        person_roles = inline_serializer(
            many=True,
            fields={
                "person": inline_serializer(
                    fields={
                        "id": serializers.IntegerField(),
                        "name": serializers.CharField()
                    }
                ),
                "role": serializers.CharField()
            }
        )

    def patch(self, request: Request, movie_id: int) -> Response:

        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        movie_service = MovieService()
        movie = movie_service.update_movie_by_id(
            movie_id=movie_id,
            data=data.validated_data,
        )

        return Response(
            data=self.OutputSerializer(movie).data,
            status=status.HTTP_201_CREATED
        )


class CustomPaginationClass(PageNumberPagination):
    page_size_query_param = 'page_size'


class MovieListAPIView(APIView):
    permission_classes = (AllowAny,)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField(max_length=250)
        year = serializers.IntegerField()
        runtime = serializers.CharField(max_length=250)
        poster = serializers.CharField(max_length=250)
        language = serializers.CharField(max_length=250)
        country = serializers.CharField(max_length=250)
        average_rating = serializers.FloatField()
        imdbRating = serializers.FloatField()

        # plot = serializers.CharField()

        # genres = inline_serializer(
        #     many=True,
        #     fields={
        #         "id": serializers.IntegerField(),
        #         "genre": serializers.CharField(max_length=250)
        #     }
        # )
        #
        # person_roles = inline_serializer(
        #     many=True,
        #     fields={
        #         "person": inline_serializer(
        #             fields={
        #                 "id": serializers.IntegerField(),
        #                 "name": serializers.CharField()
        #             }
        #         ),
        #         "role": serializers.CharField()
        #     }
        # )

    def get(self, request: Request, *args, **kwargs):

        request_params = request.GET

        movie_service = MovieService()
        movies = movie_service.get_all_movies(request_params=request_params)

        paginator = CustomPaginationClass()
        paginated_movies = paginator.paginate_queryset(movies, request)

        return paginator.get_paginated_response(
            data=self.OutputSerializer(paginated_movies, many=True).data
        )


class MovieDetailAPIView(APIView):
    permission_classes = (AllowAny,)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField(max_length=250)
        year = serializers.IntegerField()
        released = serializers.CharField(max_length=250)
        runtime = serializers.CharField(max_length=250)
        awards = serializers.CharField(max_length=250)
        poster = serializers.CharField(max_length=250)
        language = serializers.CharField(max_length=250)
        country = serializers.CharField(max_length=250)
        average_rating = serializers.FloatField()
        imdbRating = serializers.FloatField()

        plot = serializers.CharField()

        genres = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "genre": serializers.CharField(max_length=250)
            }
        )

        person_roles = inline_serializer(
            many=True,
            fields={
                "person": inline_serializer(
                    fields={
                        "id": serializers.IntegerField(),
                        "name": serializers.CharField()
                    }
                ),
                "role": serializers.CharField()
            }
        )

        comments = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "text": serializers.CharField(max_length=500),
                "rating": serializers.IntegerField(),
                "user": inline_serializer(
                    fields={
                        "id": serializers.IntegerField(),
                        "username": serializers.CharField()
                    }
                )
            }
        )

    def get(self, request: Request, movie_id: int) -> Response:

        movie_service = MovieService()
        movie = movie_service.get_movie_by_id(movie_id)

        return Response(
            data=self.OutputSerializer(movie).data,
            status=status.HTTP_200_OK
        )

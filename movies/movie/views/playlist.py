
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework import status, serializers
from rest_framework.views import APIView

from movie.services.playlist import PlaylistService


class AddToPlaylistAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, movie_id: int):

        playlist_service = PlaylistService()

        playlist_service.add_movie_by_id(
            user=request.user,
            movie_id=movie_id
        )

        return Response (
            data={
                "detail": f"The movie with ID-{movie_id} "
                          f"has been successfully added to the playlist"
            },
            status=status.HTTP_201_CREATED
        )


class DeleteFromPLaylisAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request: Request, movie_id: int) -> Response:

        playlist_service = PlaylistService()

        playlist_service.delete_movie_from_playlist_by_id(user=request.user, movie_id=movie_id)

        return Response(
            data={
                "detail": f"The movie with ID-{movie_id} "
                          f"has been successfully deleted from the playlist"
            },
            status=status.HTTP_200_OK
        )


class PlaylistAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField(source='movie.id')
        title = serializers.CharField(source='movie.title')
        year = serializers.IntegerField(source='movie.year')

    def get(self, request: Request, *args, **kwargs) -> Response:

        playlist_service = PlaylistService()
        playlist = playlist_service.show_all(request=request)

        return Response(
            data=self.OutputSerializer(playlist, many=True).data,
            status=status.HTTP_200_OK
        )


class GetRecommendationAPIView(APIView):
    permission_classes = (IsAuthenticated,)

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

    def get(self, request: Request) -> Response:

        playlist_service = PlaylistService()
        recommendations = playlist_service.get_recommendations(user_id=request.user.id)

        return Response(
            data=self.OutputSerializer(recommendations, many=True).data,
            status=status.HTTP_200_OK
        )
















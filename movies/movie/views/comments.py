from django.http import QueryDict
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from movie.common.utils import inline_serializer
from movie.services.comments import CommentService


class CommentCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        text = serializers.CharField(max_length=500)
        rating = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        text = serializers.CharField(max_length=500)
        rating = serializers.IntegerField()

        movie = inline_serializer(
                    fields={
                        "id": serializers.IntegerField(),
                        "title": serializers.CharField(),
                        "year": serializers.IntegerField()
                    }
                )

    def post(self, request: Request, movie_id: int) -> Response:

        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        comment_service = CommentService()

        person = comment_service.create_comment(
            text=data.validated_data.get('text'),
            rating=data.validated_data.get('rating'),
            movie_id=movie_id,
            author=request.user
        )

        return Response(
            data=self.OutputSerializer(person).data,
            status=status.HTTP_201_CREATED
        )


class CommentDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request: Request, comment_id: int) -> Response:

        comment_service = CommentService()

        comment_service.delete_comment_by_id(comment_id=comment_id, author_id=request.user.id)

        return Response(
            data={
                "detail": f"The comment with ID-{comment_id} "
                          f"has been successfully deleted from the comments"
            },
            status=status.HTTP_200_OK
        )


class CommentUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        text = serializers.CharField(max_length=500)
        rating = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        text = serializers.CharField(max_length=500)
        rating = serializers.IntegerField()

        movie = inline_serializer(
                    fields={
                        "id": serializers.IntegerField(),
                        "title": serializers.CharField(),
                        "year": serializers.IntegerField()
                    }
                )

    def patch(self, request: Request, comment_id: int) -> Response:

        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        comment_service = CommentService()
        comment = comment_service.update_comment_by_id(
            comment_id=comment_id,
            data=data.validated_data,
            author_id=request.user.id
        )

        return Response(
            data=self.OutputSerializer(comment).data,
            status=status.HTTP_200_OK
        )


class CommentListAPIView(APIView):

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        text = serializers.CharField(max_length=500)
        rating = serializers.IntegerField()

        user = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "username": serializers.CharField()
            }
        )

        movie = inline_serializer(
                    fields={
                        "id": serializers.IntegerField(),
                        "title": serializers.CharField(),
                        "year": serializers.IntegerField()
                    }
                )

    def get(self, request: Request, movie_id: int) -> Response:

        request_params: QueryDict = request.GET

        comment_service = CommentService()
        comments = comment_service.get_all_comments(request_params=request_params, movie_id=movie_id)

        return Response(
            data=self.OutputSerializer(comments, many=True).data,
            status=status.HTTP_200_OK
        )






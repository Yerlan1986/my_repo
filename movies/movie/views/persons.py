from django.http import QueryDict
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.request import Request

from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from movie.common.utils import inline_serializer
from movie.services.persons import PersonService


class PersonListAPIView(APIView):
    permission_classes = (AllowAny,)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField(max_length=250)

        movies = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "title": serializers.CharField(),
                "year": serializers.IntegerField()
            }
        )

    def get(self, request: Request, *args, **kwargs) -> Response:

        request_params: QueryDict = request.GET

        person_service = PersonService()
        persons = person_service.get_all_persons(request_params=request_params)

        return Response(
            data=self.OutputSerializer(persons, many=True).data,
            status=status.HTTP_200_OK
        )


class PersonDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def delete(self, request: Request, person_id: int) -> Response:

        person_service = PersonService()

        person_service.delete_person_by_id(person_id=person_id)

        return Response(
            data={
                "detail": f"The person with ID-{person_id} "
                          f"has been successfully deleted from the list"
            },
            status=status.HTTP_200_OK
        )


class PersonUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=250, required=False)
        birth_date = serializers.DateField(required=False)
        biography = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField(max_length=250)
        birth_date = serializers.DateField()
        biography = serializers.CharField()

    def patch(self, request: Request, person_id: int) -> Response:

        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        person_service = PersonService()
        person = person_service.update_person_by_id(
            person_id=person_id,
            data=data.validated_data,
        )

        return Response(
            data=self.OutputSerializer(person).data,
            status=status.HTTP_200_OK
        )


class PersonDetailAPIView(APIView):
    permission_classes = (AllowAny,)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField(max_length=250)
        birth_date = serializers.DateField()
        biography = serializers.CharField()

        movies = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "title": serializers.CharField(),
                "year": serializers.IntegerField()
            }
        )

    def get(self, request: Request, person_id: int) -> Response:

        person_service = PersonService()
        person = person_service.get_person_by_id(person_id)

        return Response(
            data=self.OutputSerializer(person).data,
            status=status.HTTP_200_OK
        )


class PersonCreateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=250)
        birth_date = serializers.DateField(required=False)
        biography = serializers.CharField(required=False)
        role = serializers.CharField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField(max_length=250)
        birth_date = serializers.DateField()
        biography = serializers.CharField()

        movies = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "title": serializers.CharField(),
                "year": serializers.IntegerField()
            }
        )

    def post(self, request: Request, movie_id: int) -> Response:

        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        person_service = PersonService()

        person = person_service.create_person(
            name=data.validated_data.get('name'),
            birth_date=data.validated_data.get('birth_date'),
            biography=data.validated_data.get('biography'),
            role=data.validated_data.get('role'),
            movie_id=movie_id
        )

        return Response(
            data=self.OutputSerializer(person).data,
            status=status.HTTP_201_CREATED
        )









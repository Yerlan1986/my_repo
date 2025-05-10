
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authorization.constants import ROLE_ADMIN, ROLE_USER, ROLE_MODERATOR

ROLE_CHOICES = [ROLE_ADMIN, ROLE_USER, ROLE_MODERATOR]


class HealthApiView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        print("Get request was sent by:", request.user)

        return HttpResponse("Ok!")


class LoginApiView(APIView):
    permission_classes = (AllowAny,)

    class InputSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=150)
        password = serializers.CharField(max_length=150)

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data.get("username"),
            password=serializer.validated_data.get("password")
        )

        if user:
            login(request, user)
        else:
            return Response({"message": "Invalid credentials!"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Login successful!"})


class LogoutApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logout successful!"})


class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)

    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        username = serializers.CharField(max_length=255)
        first_name = serializers.CharField(allow_blank=True, allow_null=True)
        last_name = serializers.CharField(allow_blank=True, allow_null=True)
        role = serializers.ChoiceField(choices=ROLE_CHOICES)
        created_at = serializers.DateTimeField()

    def post(self, request, *args, **kwargs):

        serializer = self.InputSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            User = get_user_model()
            user = User.objects.create(
                username=serializer.validated_data["username"],
                password=make_password(serializer.validated_data["password"])
            )

        return Response(self.OutputSerializer(user).data)


class MeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        username = serializers.CharField(max_length=255)
        first_name = serializers.CharField(allow_blank=True, allow_null=True)
        last_name = serializers.CharField(allow_blank=True, allow_null=True)
        email = serializers.EmailField(allow_blank=True, allow_null=True)
        role = serializers.ChoiceField(choices=ROLE_CHOICES)
        created_at = serializers.DateTimeField()

    def get(self, request, *args, **kwargs):
        return Response(self.OutputSerializer(request.user).data)


class UpdateUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        first_name = serializers.CharField(required=False, allow_blank=True)
        last_name = serializers.CharField(required=False, allow_blank=True)
        email = serializers.EmailField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        username = serializers.CharField()
        first_name = serializers.CharField(allow_blank=True, allow_null=True)
        last_name = serializers.CharField(allow_blank=True, allow_null=True)
        email = serializers.EmailField(required=False)
        role = serializers.ChoiceField(choices=ROLE_CHOICES)
        created_at = serializers.DateTimeField()

    def put(self, request: Request, *args, **kwargs):

        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data = data.validated_data

        user = get_user_model().objects.get(id=request.user.id)

        if data.get("first_name"):
            user.first_name = data.get("first_name")
        if data.get("last_name"):
            user.last_name = data.get("last_name")
        if data.get("email"):
            user.email = data.get("email")

        user.save()
        return Response(
            data=self.OutputSerializer(user).data,
            status=status.HTTP_200_OK
        )


class DeleteUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        request.user.delete()
        return Response(
            data={"message": "User deleted successfully."},
            status=status.HTTP_200_OK
        )


class ChangePasswordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        old_password = serializers.CharField()
        new_password = serializers.CharField(min_length=6)

    def post(self, request: Request, *args, **kwargs) -> Response:

        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        user = request.user

        if data.is_valid(raise_exception=True):
            hashed_password = make_password(data.validated_data.get('new_password'))

            user.password = hashed_password
            user.save()

        return Response(
            data={"message": "Password changed successfully."},
            status=status.HTTP_200_OK
        )


class UserListAPIView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        username = serializers.CharField()
        role = serializers.ChoiceField(choices=ROLE_CHOICES)
        created_at = serializers.DateTimeField()

    def get(self, request: Request, *args, **kwargs) -> Response:

        users = get_user_model().objects.all()

        return Response(
            data=self.OutputSerializer(users, many=True).data,
            status=status.HTTP_200_OK
        )




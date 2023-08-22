from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import (
    status,
)
from .serializers import (
    UserRegistrationSerializer,
    CustomTokenSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserStatusUpdateSerializer
)
from account.models import (
    User
)
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group

# Register Users


class UserRegistration(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.create(
                    validated_data=serializer.validated_data)
                token = CustomTokenSerializer.get_token(user)
                context = {
                    "status": status.HTTP_201_CREATED,
                    "success": True,
                    "response": "Successfully Registered!",
                    "refresh": str(token),
                    "access": str(token.access_token),
                    "username": user.username,
                    "email": user.email,
                    "user_uid": user.uid
                }
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                context = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success": False,
                    "response": serializer.errors
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            context = {
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "response": str(exception)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


# Login Users
class UserLogin(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = authenticate(
                    email=serializer.data['email'], password=serializer.data['password'])
                if user != None:
                    token = CustomTokenSerializer.get_token(user)
                    context = {
                        "status": status.HTTP_200_OK,
                        "success": True,
                        "erros_status": False,
                        "response": "Successfully Logged In!",
                        "refresh": str(token),
                        "access": str(token.access_token),
                        "username": user.username,
                        "email": user.email,
                        "uid": user.uid,
                        "user_type": user.groups.first().name

                    }
                    return Response(context, status=status.HTTP_200_OK)
                else:
                    context = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "success": False,
                        "erros_status": True,
                        "response": {
                            "error": "Unable to log in with provided credentials!"
                        }
                    }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            else:
                serializer_errors = {key: value[0]
                                     for key, value in serializer.errors.items()}
                context = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success": False,
                    "erros_status": True,
                    "response": {
                        "error": list(serializer_errors.values())[0] + "!"
                    }
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            context = {
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "erros_status": True,
                "response": {
                    "error": str(exception) + "!",
                }
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


# User Groups
class UserGroup(APIView):
    def get(self, request, *args, **kwargs):
        # for web api
        try:
            user_group_qs = Group.objects.exclude(
                name="Field Executive").values("id", "name")
            context = {
                "status": status.HTTP_200_OK,
                "success": True,
                "response": user_group_qs
            }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as exception:
            context = {
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "response": str(exception)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


# Get Users With User Group
class UsersWithGroup(APIView):
    def get(self, request, *args, **kwargs):
        try:
            get_user_type = request.GET.get('user_type', None)
            if get_user_type is not None:
                user_qs = User.objects.filter(
                    groups__name__iexact=get_user_type)
                serializer = UserSerializer(user_qs, many=True)
                context = {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "response": serializer.data
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success": False,
                    "response": "you have to pass user type!"
                }
                return Response(context, status=status.HTTP_200_OK)
        except Exception as exception:
            context = {
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "response": str(exception),
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

# Update the active or in active attribute of users


class UserStatus(APIView):
    def put(self, request, uid):
        try:
            data = request.data
            user_instance = User.objects.get(uid=uid)
            serializer = UserStatusUpdateSerializer(
                user_instance, data=data, partial=True,
            )
            if serializer.is_valid():
                serializer.save()
                context = {
                    'status': status.HTTP_200_OK,
                    'success': True,
                    'response': serializer.data
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                serializer_errors = {key: value[0]
                                     for key, value in serializer.errors.items()}
                context = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success": False,
                    "response": {
                        "error": list(serializer_errors.values())[0] + "!"
                    }
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            context = {
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "response": str(exception),
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

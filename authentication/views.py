from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .seriallizers import UserSerializer, UserLoginSerializer, UserRegisterSerializer, UserProfileSerializer
from Users.models import User, Doctor, Patient, Admin
from django.contrib.auth import login, logout
from rest_framework import status


class signin(APIView):
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            user = serializer.check_user(data)
            login(request, user)
            return Response({"message": "access granted", }, status=status.HTTP_201_CREATED)
        return Response({"message": "Username or password invalid"}, status=status.HTTP_400_BAD_REQUEST)


class signup(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            userid = User.objects.create_user(username=request.data['username'],
                                              password=request.data['password'],
                                              email=request.data['email'],
                                              is_superuser=request.data['is_superuser'],
                                              is_staff=request.data['is_staff']
                                              ).pk
            user = User.objects.get(username=request.data['username'])
            token = Token.objects.create(user=user)
            if request.data['is_superuser']:
                Admin.objects.create(User_id=userid)
            elif request.data['is_staff']:
                Doctor.objects.create(User_id=userid)
            else:
                Patient.objects.create(User_id=userid)
            return Response(
                {"message": "User created successfully ", "token": token.key},
                status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class signout(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class userList(APIView):
    def get(self, request):
        users = User.objects.all()
        users = UserSerializer(users, many=True).data
        return Response({'users': users}, status=status.HTTP_200_OK)


class userDetail(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        user = UserSerializer(user).data
        return Response({'user': user}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response({'message': 'User Deleted Successfully'}, status=status.HTTP_200_OK)

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

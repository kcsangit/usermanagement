from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import *
import uuid
from django.contrib.auth import login
from userapp.email import activate
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from userapp.models import User
from userapp.serializers import UserListSerializer, UserSerializer, TokenVerifySerializer, EmailCheckSerializer, ForgetPasswordSerializer, change_passwordSerializer
from rest_framework import permissions


# class Permission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method == 'POST':
#             return True
#         return request.user and request.user.is_authenticated

# class IsPostOrIsAuthenticated(permissions.BasePermission):

#     def has_permission(self, request, view):
#       return request.user and request.user.is_authenticated

class UserAPIView(APIView):
    # permission_classes = (Permission ,)
    serializer_class = UserSerializer

    def get(self, request):
        user_object = User.objects.all()
        serializer = UserListSerializer(
            user_object, many=True, context={'request': request})
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['password'] == serializer.validated_data['confirm_password']:
                token = uuid.uuid4().hex[:6].upper()
                user_object = User()
                user_object.first_name = serializer.validated_data['first_name']
                user_object.middle_name = serializer.validated_data['middle_name']
                user_object.last_name = serializer.validated_data['last_name']
                user_object.email = serializer.validated_data['email']
                user_object.phone_number = serializer.validated_data['phone_number']
                user_object.image = serializer.validated_data['image']
                user_object.password = serializer.validated_data['password']
                user_object.usertype = serializer.validated_data['usertype']
                user_object.token = token
                user_object.save()
                text_content = 'Account Activation Email'
                template_name = 'activation.html'
                subject = 'Email Activation'
                first_name = serializer.validated_data['first_name']
                email = serializer.validated_data['email']
                activate(email, text_content, template_name,
                         subject, token, first_name)
                return Response({"Account Sucessfully created."}, status=200)
            return Response({"Password doesn't matched."}, status=400)
        return Response(serializer.errors, status=400)


class UserUpdateAPIView(APIView):

    serializer_class = UserSerializer

    def get(self, request, id):
        user_object = User.objects.filter(id=id)
        if user_object:
            user_object = User.objects.get(id=id)
            if user_object.id == request.user.id:
                serializer = UserListSerializer(
                    user_object, many=False, context={'request': request})
                return Response(serializer.data, status=200)
            return Response({"You are not allowed."}, status=400)
        return Response({"User not found."}, status=400)

    def put(self, request, id):
        user_object = User.objects.filter(id=id)
        if user_object:
            user_object = User.objects.get(id=id)
            if user_object.id == request.user.id:
                user_object.first_name = request.data['first_name']
                user_object.middle_name = request.data['middle_name']
                user_object.last_name = request.data['last_name']
                user_object.email = request.data['email']
                user_object.phone_number = request.data['phone_number']
                user_object.image = request.data['image']
                user_object.usertype = request.data['usertype']
                user_object.update_password = False
                user_object.save()

                return Response({"Sucessfully Edited."}, status=200)
            return Response({"You are not allowed."}, status=400)
        return Response({"User not found."}, status=400)

    def delete(self, request, id):
        # permission_classes = (IsPostOrIsAuthenticated ,)

        user_object = User.objects.filter(id=id)
        if user_object:
            user_object = User.objects.get(id=id)
            if user_object.id == request.user.id:
                user_object.delete()
                return Response({"Sucessfully deleted."}, status=200)
            return Response({"You don't have access"}, status=400)
        return Response({"User not found."}, status=400)


class TokenverifyAPI(APIView):

    serializer_class = TokenVerifySerializer

    def post(self, request):
        serializer = TokenVerifySerializer(data=request.data)
        if serializer.is_valid():
            user_object = User.objects.filter(
                token=serializer.validated_data['token'])
            if user_object:
                user_object = User.objects.get(
                    token=serializer.validated_data['token'])
                user_object.active = True
                user_object.update_password = False
                user_object.token = None
                user_object.save()
                return Response({"Token Verified."}, status=200)
            return Response({"Token invalid."}, status=400)
        return Response(serializer.errors, status=400)


class ForgetPasswordAPI(APIView):
    # permission_classes = (IsPostOrIsAuthenticated ,)
    serializer_class = EmailCheckSerializer

    def post(self, request):
        token = uuid.uuid4().hex[:6].upper()

        user_object = User.objects.filter(email=request.data['email'])
        if user_object:
            user_object = User.objects.get(email=request.data['email'])
            user_object.token = token
            user_object.save()
            text_content = 'Account Activation Email'
            template_name = 'activation.html'
            subject = 'Email Activation'
            first_name = user_object.first_name
            email = request.data['email']
            activate(email, text_content, template_name,
                     subject, token, first_name)
            return Response({"Password Reset Code is send to your mail."}, status=200)
        return Response({"Email is not found."}, status=400)


class ResetPasswordAPI(APIView):
    # permission_classes = (IsPostOrIsAuthenticated ,)
    serializer_class = ForgetPasswordSerializer

    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user_object = User.objects.filter(
                token=serializer.validated_data['token'])
            if user_object:
                if serializer.validated_data['change_password'] == serializer.validated_data['confirm_password']:
                    user_object = User.objects.get(
                        token=serializer.validated_data['token'])
                    user_object.set_password(
                        serializer.validated_data['confirm_password'])
                    user_object.update_password = False
                    user_object.token = None
                    user_object.save()
                    return Response({"Password is successfully reset."}, status=200)
                return Response({"Password doesnot matched."}, status=400)
            return Response({"Token doesn't matched."}, status=400)
        return Response(serializer.errors, status=400)


class change_passwordAPI(APIView):
    # permission_classes = (IsPostOrIsAuthenticated ,)
    serializer_class = change_passwordSerializer

    def post(self, request):
        serializer = change_passwordSerializer(data=request.data)
        if serializer.is_valid():
            user_object = User.objects.get(id=request.user.id)
            user_id = user_object.id
            user_check = user_object.check_password(
                serializer.validated_data['password'])
            if user_check:
                if serializer.validated_data['change_password'] == serializer.validated_data['confirm_password']:
                    user_object.set_password(
                        serializer.validated_data['confirm_password'])
                    user_object.update_password = False
                    user_object.save()
                    user_object = User.objects.get(id=user_id)
                    login(request, user_object)
                    return Response({"Sucessfully password changed."}, status=200)
                return Response({"password doesn't matched."}, status=400)
            return Response({"Current password doesn't matched."}, status=400)
        return Response(serializer.errors, status=400)

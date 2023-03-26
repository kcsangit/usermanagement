from rest_framework import serializers
from userapp.models import  User



class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'email',
                  'phone_number', 'image', 'active', 'usertype']


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'email',
                  'phone_number', 'image', 'usertype', 'password', 'confirm_password']


class TokenVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['token', ]


class EmailCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', ]


class ForgetPasswordSerializer(serializers.ModelSerializer):
    change_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['token', 'change_password', 'confirm_password']


class change_passwordSerializer(serializers.ModelSerializer):
    change_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['password', 'change_password', 'confirm_password']

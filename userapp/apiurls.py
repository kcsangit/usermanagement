from django.urls import path, include
from userapp.api import UserAPIView, UserUpdateAPIView, TokenverifyAPI, ForgetPasswordAPI, ResetPasswordAPI, change_passwordAPI

urlpatterns = [
    path('users', UserAPIView.as_view()),
    path('users/<id>', UserUpdateAPIView.as_view()),

    path('user-activate/', TokenverifyAPI.as_view()),
    path('forgetpassword', ForgetPasswordAPI.as_view()),
    path('resetpassword', ResetPasswordAPI.as_view()),
    path('changepassword', change_passwordAPI.as_view()),

]

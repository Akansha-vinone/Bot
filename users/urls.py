from django.urls import path
from . import views

urlpatterns = [
    path('',views.login, name='login'),
    path('login/',views.login, name='login'),
    path('register/',views.register),
    path('chat/',views.chatBot,name='chatBot'),
    path('thankyou/',views.Thankyou,name='Thankyou'),
    path('ForgetPassword/',views.forgetPassword,name='forgetPassword'),
    path('newPasswordPage/<str:user>',views.NewPasswordPage,name='NewPasswordPage')
]
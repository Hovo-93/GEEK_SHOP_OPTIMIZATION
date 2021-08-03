from django.contrib import auth
from django.urls import path

import users.views as users
from users.views import login, registration, profile, logout,send_verify_mail

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('verify/<email>/<activation_key>/', users.verify,name='verify')
]

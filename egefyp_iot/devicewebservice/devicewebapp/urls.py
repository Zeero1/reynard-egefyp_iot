from django.urls import path
from devicewebapp import views
from rest_framework.authtoken import views

#TEMPLATE URLS
app_name = 'devicewebapp'

urlpatterns=[
    path('',views.index,name='index'),
    path('register/',views.register, name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('mac_add/',views.command_view,name='mac_add'),
    path('hello/',views.hello, name='hello'),
]

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]

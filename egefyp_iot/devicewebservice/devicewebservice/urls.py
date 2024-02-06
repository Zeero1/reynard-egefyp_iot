"""devicewebservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from devicewebapp import views
from django.conf import settings #add this
from django.conf.urls.static import static #add this

from rest_framework.authtoken import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='index'),
    path('devicewebapp/',include('devicewebapp.urls')),
    path('logout/',views.user_logout, name='logout'),
    path('viewdevices/',views.viewdevices,name='viewdevices'),
    path('devices/<str:param1>',views.devices,name='devices'),
    path('postd/',views.postview,name='postview'),
    path('messageview/',views.messageview,name='messageview'),
    path('motoron/',views.activatemotorview,name='activatemotorview'),
    #path('',include('django_socketio.urls')),
    #(?P<first_name>[a-zA-Z]+)/(?P<last_name>[a-zA-Z]+)(?:/(?P<title>[a-zA-Z]+))?/$'
]

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

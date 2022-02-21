"""coolsite URL Configuration

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
from django.conf.urls import handler404
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static



from women.views import *
from django.urls import include #для представления переходов в упрощенном варианте

from . import settings

urlpatterns = [  
    path('admin/', admin.site.urls),  
    path('', include('women.urls')) #http://127.0.0.1:8000/
    ]


if settings.DEBUG: #в режиме отладки добавляем новый маршрут
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns = [
#    path('admin/', admin.site.urls),
#    path('women/', index), #http://127.0.0.1:8000/ домен +women-на выходе http://127.0.0.1:8000/women/
#    path('', index), #http://127.0.0.1:8000/
#    path('cats/', categories) #http://127.0.0.1:8000/cats/ 
#]

#Обработка 404

handler404 = pageNotFound
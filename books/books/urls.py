from django.contrib import admin

from django.urls import include, re_path
from django.urls import path
from rest_framework.routers import SimpleRouter

from store.views import *

router = SimpleRouter()
router.register(r'book', BookViewSet)  # http://127.0.0.1:8000/book/?format=json

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', include('social_django.urls', namespace='social')),
    path('auth/', auth)



]
urlpatterns += router.urls

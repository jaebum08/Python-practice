
from django.conf.urls import url, include


urlpatterns = [
    url(r'^', include('apps.main_app.urls')),
]
from django.urls import path

from commerce.views import v1


urlpatterns = [
    path('v1/test', v1.index),
]

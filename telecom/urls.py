from django.conf.urls import include, url
from django.contrib import admin
from views import HomeView, EstimateView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^estimate/$', EstimateView.as_view(), name='estimate'),
]

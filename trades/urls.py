from django.urls import path
from . import views, api_views

urlpatterns = [
    path("", views.index, name="index"),                               
    path("validate/", api_views.validate_trade, name="validate"),        
    path("api/load_rosters/", api_views.load_rosters, name="load_rosters"),
]

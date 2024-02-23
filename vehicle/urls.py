from django.contrib import admin
from django.urls import path
from vehicle import views
from .views import get_vehicle_details,get_checout,get_vehicle_quality,RegiserAPI,LoginAPI
from .views import initiate_checkout_api,conduct_quality_check_api,add_vehicle_api
urlpatterns = [
    path('api/register/',RegiserAPI.as_view()),
    # path('api/verify/',VerifyOTP.as_view()),
    #path for getting the details of a particular vehicle by its id
    path('api/login/',LoginAPI.as_view()),
    path('api/vehicle/<int:vehicle_id>/', get_vehicle_details, name='get_vehicle_details'),
    path('api/vehical_quality/<int:vehicle_id>/', get_vehicle_quality, name='get_vehicle_details'),
    path('api/vehicle_checkout/<int:vehicle_id>/', get_checout, name='get_vehicle_details'),
    path('api/add_vehicle/', add_vehicle_api, name='add_vehicle_api'),
    path('api/quality_check/<int:vehicle_id>/', conduct_quality_check_api, name='conduct_quality_check_api'),
    path('api/checkout/<int:vehicle_id>/', initiate_checkout_api, name='initiate_checkout_api'),
]

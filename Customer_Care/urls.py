from django.urls import path
from . import views

urlpatterns = [

     path("api-get-customer-service-details/", views.get_customer_service),

]

from django.urls import path
from . import views
from .views import AuthToken, UserCreate, UpdateProfile
urlpatterns = [

      path('api-login/', AuthToken.as_view()),
      path("api-get-profile/", views.user_profile),
      path("api-email-check/", views.Email_check.as_view()),
      path("api-update-profile/", UpdateProfile.as_view()),
      path('api-user-register/', UserCreate.as_view())

]





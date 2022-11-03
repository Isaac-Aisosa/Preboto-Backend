from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from preboto import settings
from . import views
from .views import *
urlpatterns = [

          path('', views.index, name='index'),
          path('policy', views.policy, name='policy'),
          path('about', views.about, name='about'),
          ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)





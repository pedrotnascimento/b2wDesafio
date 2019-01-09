from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from starwars import views

urlpatterns = [
    path('planets/', views.PlanetList.as_view()),
    path('planets/<int:pk>/', views.PlanetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

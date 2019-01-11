from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from starwars import views

urlpatterns = [
    path('planets/', views.PlanetList.as_view()),
    path('planets/<int:pk>/', views.PlanetDetail.as_view()),
    url(r'^docs/', include_docs_urls(title='B2W Star Wars API'))
]

urlpatterns = format_suffix_patterns(urlpatterns)

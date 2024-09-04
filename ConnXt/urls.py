from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home),
    path('talent/', views.talent, name = 'talent'),
    path('profile/', views.profile),
    path('employer/', views.employer),
    path('jobs/', views.jobs),
    path('studentdash/', views.studentdash),
    path('aboutus/', views.aboutus),
    path('studenterror/', views.studenterror),
    path('employererror/', views.employererror),
]
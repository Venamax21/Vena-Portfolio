from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name = 'home'), #Home page
    path('about/', views.about, name='about'),
    path('project/', views.project, name='project'),
    path('contact/', views.contact, name='contact'),
    path('sendmail/', views.sendmail, name='sendmail'),  # <-- Vue endpoint
]
from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.home, name='fr-home'),
    path('create/', views.create, name='fr-create'),
    path('<int:id>/', views.get, name='fr-get'),
    path('update/<int:id>/', views.update, name='fr-update'),
    path('delete/<int:id>/', views.delete, name='fr-delete'),
]

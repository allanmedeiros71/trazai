from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('lists/<int:pk>/', views.list_detail, name='list_detail'),
    path('lists/<int:pk>/add/', views.add_item, name='add_item'),
    path('items/<int:item_id>/toggle/', views.toggle_item, name='toggle_item'),
]

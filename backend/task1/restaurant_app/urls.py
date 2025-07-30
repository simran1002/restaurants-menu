from django.urls import path
from . import views

app_name = 'restaurant_app'

urlpatterns = [
    # Restaurant CRUD operations
    path('restaurants/', views.RestaurantListCreateView.as_view(), name='restaurant-list-create'),
    path('restaurants/<int:pk>/', views.RestaurantDetailView.as_view(), name='restaurant-detail'),
    
    # Additional endpoint for statistics
    path('restaurants/stats/', views.restaurant_stats, name='restaurant-stats'),
]

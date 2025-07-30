from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.db import models
from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantListCreateView(generics.ListCreateAPIView):
    
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    'success': True,
                    'message': 'Restaurant created successfully',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        return Response(
            {
                'success': False,
                'message': 'Validation failed',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                'success': True,
                'count': len(serializer.data),
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )


@api_view(['GET'])
def restaurant_stats(request):
    
    total_restaurants = Restaurant.objects.count()
    if total_restaurants > 0:
        avg_rating = Restaurant.objects.aggregate(
            avg_rating=models.Avg('rating')
        )['avg_rating']
        highest_rated = Restaurant.objects.order_by('-rating').first()
        lowest_rated = Restaurant.objects.order_by('rating').first()
        
        return JsonResponse({
            'success': True,
            'stats': {
                'total_restaurants': total_restaurants,
                'average_rating': round(float(avg_rating), 2) if avg_rating else 0,
                'highest_rated': {
                    'name': highest_rated.name,
                    'rating': float(highest_rated.rating)
                } if highest_rated else None,
                'lowest_rated': {
                    'name': lowest_rated.name,
                    'rating': float(lowest_rated.rating)
                } if lowest_rated else None
            }
        })
    else:
        return JsonResponse({
            'success': True,
            'stats': {
                'total_restaurants': 0,
                'average_rating': 0,
                'highest_rated': None,
                'lowest_rated': None
            }
        })

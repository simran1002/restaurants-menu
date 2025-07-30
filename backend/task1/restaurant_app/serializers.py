from rest_framework import serializers
from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer for Restaurant model with validation
    """
    
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone_number', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_rating(self, value):
        """
        Validate that rating is between 0.0 and 5.0
        """
        if value < 0.0 or value > 5.0:
            raise serializers.ValidationError("Rating must be between 0.0 and 5.0")
        return value
    
    def validate_phone_number(self, value):
        """
        Basic phone number validation
        """
        if not value.strip():
            raise serializers.ValidationError("Phone number cannot be empty")
        return value.strip()
    
    def validate_name(self, value):
        """
        Validate restaurant name
        """
        if not value.strip():
            raise serializers.ValidationError("Restaurant name cannot be empty")
        return value.strip()

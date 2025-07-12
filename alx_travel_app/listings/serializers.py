from rest_framework import serializers
from .models import Listing, Booking

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'price_per_night', 'location', 'created_at']

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    listing = serializers.StringRelatedField()

    class Meta:
        model = Booking
        fields = ['id', 'user', 'listing', 'check_in', 'check_out', 'status']
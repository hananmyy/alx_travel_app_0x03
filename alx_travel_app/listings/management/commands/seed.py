from django.core.management.base import BaseCommand
from listings.models import Listing

class Command(BaseCommand):
    help = "Seed the database with sample listings"

    def handle(self, *args, **kwargs):
        sample_listings = [
            {"title": "Luxury Beach House", "description": "Ocean views.", "price_per_night": 200, "location": "Malindi"},
            {"title": "Cozy Mountain Cabin", "description": "Cabin in the mountains.", "price_per_night": 150, "location": "Mt. Kenya"},
            {"title": "City Apartment", "description": "Modern apartment in Nairobi.", "price_per_night": 100, "location": "Nairobi CBD"}
        ]
        
        for listing_data in sample_listings:
            Listing.objects.create(**listing_data)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
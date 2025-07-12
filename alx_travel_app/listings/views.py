from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
import uuid
import requests
from django.conf import settings
from .tasks import send_payment_confirmation_email



class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@api_view(['POST'])
def initiate_payment(request, booking_id):
    try:
        booking = Booking.objects.get(pk=booking_id)
        tx_ref = f"booking-{booking.id}-{uuid.uuid4().hex[:6]}"
        chapa_url = "https://api.chapa.co/v1/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET}"
        }
        payload = {
            "amount": str(booking.listing.price_per_night),
            "currency": "ETB",
            "email": booking.user.email,
            "tx_ref": tx_ref,
            "first_name": booking.user.first_name,
            "last_name": booking.user.last_name,
            "callback_url": "https://yourdomain.com/chapa-webhook/",
            "return_url": "https://yourdomain.com/payment-success/"
        }

        response = requests.post(chapa_url, headers=headers, json=payload)
        data = response.json()

        if data.get("status") == "success":
            Payment.objects.create(
                booking=booking,
                amount=booking.listing.price_per_night,
                status="Pending",
                transaction_id=tx_ref
            )
            return Response({"checkout_url": data["data"]["checkout_url"]})
        else:
            return Response({"error": "Failed to initialize payment", "details": data}, status=400)

    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=404)
    

@api_view(['GET'])
def verify_payment(request, tx_ref):
    import requests
    from .models import Payment
    from .tasks import send_payment_confirmation_email  # <-- import the task here

    chapa_url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET}"
    }

    response = requests.get(chapa_url, headers=headers)
    data = response.json()

    try:
        payment = Payment.objects.get(transaction_id=tx_ref)
    except Payment.DoesNotExist:
        return Response({"error": "Transaction not found"}, status=404)

    if data.get("status") == "success" and data["data"].get("status") == "success":
        payment.status = "Completed"
        payment.save()

        # Send confirmation email asynchronously
        user = payment.booking.user
        print(f"Triggering email task for booking #{payment.booking.id}")
        send_payment_confirmation_email.delay(user.email, str(payment.booking.id))

        return Response({"status": "Payment successful", "data": data["data"]})
    else:
        payment.status = "Failed"
        payment.save()
        return Response({"status": "Payment failed or unverified", "data": data["data"]})
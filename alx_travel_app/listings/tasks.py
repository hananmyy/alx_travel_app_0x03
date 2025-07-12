from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_payment_confirmation_email(user_email, booking_id):
    print(f"Sending payment confirmation email to {user_email} for booking #{booking_id}")
    send_mail(
        subject="Payment Confirmation",
        message=f"Your booking #{booking_id} has been successfully paid.",
        from_email="noreply@alxtravel.com",
        recipient_list=[user_email],
        fail_silently=False,
    )
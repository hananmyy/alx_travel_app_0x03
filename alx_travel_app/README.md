# ALX Travel App — Payment Integration with Chapa

This Django-based travel booking app allows users to browse listings, make bookings, and securely pay using the Chapa API.

##  Duplicate Project  
The original project `alx_travel_app_0x01` was duplicated into `alx_travel_app_0x02` for implementing data modeling and seeding.

## Project Structure

- **Backend**: Django, Django REST Framework
- **Payments**: [Chapa API](https://developer.chapa.co/)
- **Async Tasks**: Celery (for email confirmation)


## Features

- Users can:
  - Browse and book accommodations
  - Initiate secure payments via Chapa
  - Receive confirmation emails after successful transactions

- Admin can:
  - Track payment status
  - View all booking and transaction records


## Environment Variables

Create a `.env` file or update `settings.py`:

```env
CHAPA_SECRET_KEY=your_test_or_live_key_here


## Background Task Management with Celery

To handle email notifications asynchronously, Celery is configured with RabbitMQ.

### Setup

1. Install Celery:  
   ```bash
   pip install celery
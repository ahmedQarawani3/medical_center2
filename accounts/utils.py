# accounts/utils.py
from twilio.rest import Client
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def send_sms(to_number, message_body):
    """
    Sends an SMS to the specified number using Twilio API.
    """
    required_settings = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE_NUMBER']
    for setting in required_settings:
        if not hasattr(settings, setting):
            raise ImproperlyConfigured(f"The '{setting}' is not configured in settings.")

    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message_body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_number
        )
        return message.sid
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return None

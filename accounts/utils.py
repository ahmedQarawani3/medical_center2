from twilio.rest import Client
from django.conf import settings

def send_sms(to_number, message_body):
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

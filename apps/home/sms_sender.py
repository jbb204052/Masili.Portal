from django.http import HttpResponse
from twilio.rest import Client

account_sid = 'AC9f0be1819e581d9b9210479fdc5f58db'
auth_token = 'c8fb5ba5b12083b79e8e93727959ab17'
messaging_service_sid = 'MGd0ec9bf51822bad4543f1204f17f35ba'
client = Client(account_sid, auth_token)


def send_sms(number, message):
    message = client.messages.create(
        body=message,
        from_=messaging_service_sid,
        to=number
    )
    print(message.sid)
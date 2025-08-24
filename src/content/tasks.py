from time import sleep
from celery import shared_task


@shared_task()
def send_email_task(email_address, message):

    print("now i'm supposed to send an email. It will take 20 secs.")
    sleep(20)  # Simulate expensive operation(s) that freeze Django

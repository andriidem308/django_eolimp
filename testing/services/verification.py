import random
import string

from django.core.mail import send_mail

from django_eolimp.settings import EMAIL_HOST_USER


def send_verification_passcode(email):
    passcode = generate_passcode()

    subject = 'Verify your account'
    message = "Your passcode for your account: " + passcode
    print(f'EMAIL:{email}')
    print(f'EMAILhost:{EMAIL_HOST_USER}')
    send_mail(subject, message, EMAIL_HOST_USER, [email])

    return passcode


def generate_passcode():
    length = 6
    characters = string.ascii_letters + string.digits

    random_passcode = ''.join(random.choice(characters) for _ in range(length))

    return random_passcode

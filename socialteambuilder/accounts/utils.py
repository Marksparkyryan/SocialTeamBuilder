from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_confirmation_email(user):
    token = default_token_generator.make_token(user)
    try:
        raise Exception("Put getting of current domain logic here")
    except:
        domain = 'http://127.0.0.1:8000/'
    message = render_to_string('accounts/confirm_email_template.html', {
        'user': user,
        'domain': domain,
        'user_pk': user.pk,
        'token':token,
    })
    recipient = user.email
    email = EmailMessage(
        subject='Welcome to Team Builder!',
        body=message,
        to=[user.email]
    )
    email.send()

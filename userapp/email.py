from userapp.models import User
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from django.core.mail import send_mail


def activate(email, text_content, template_name, subject, token, first_name):
    try:
        user = User.objects.get(email=email)
        from_email = settings.DEFAULT_FROM_EMAIL
        recipients = [user.email]
        context = {'user': first_name, 'token': token}
        html_content = render_to_string(template_name, context)
        email = EmailMultiAlternatives(
            subject, text_content, from_email, recipients)
        email.attach_alternative(html_content, "text/html")
        email.send()
        print("token"+token)

    except:
        print("email activate account send errror")
        # print(e)
        print("=================")
        return Response({"message": "Email does not send"}, status=400)

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


def detectUser(user):
  if user.role == 1:
    redirectUrl = 'vendorDashboard'
    return redirectUrl
  elif user.role == 2:
    redirectUrl = 'custDashboard'
    return redirectUrl
  elif user.role == None and user.is_superadmin:
    redirectUrl = '/admin'
    return redirectUrl
  else:
    redirectUrl = 'registerUser'
    return redirectUrl
  

#HELPER FUNCTION TO SEND THE VERIFICATION EMAIL.
def send_verification_email(request,user):
  from_email = settings.DEFAULT_FROM_EMAIL
  current_site = get_current_site(request) #FIRST WE GET THE CURRENT SITE.
  mail_subject = 'Activate your account.'
  message = render_to_string('accounts/emails/account_verification_email.html',{
    'user':user,
    'domain':current_site,
    'uid':urlsafe_base64_encode(force_bytes(user.pk)), #TO ENCODE THE USER PRIMARY KEY.
    'token':default_token_generator.make_token(user),   
  })  
  to_email = user.email
  mail = EmailMessage(mail_subject, message, from_email, [to_email])
  mail.send()

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.core.mail import send_mail
from django.conf import settings

from .models import Profile

# Signals allow certain senders to notify a set of receivers that some action had taken place

# createProfile and deleteUser is a receiver
# post_save and post_delete is a signal

# signals file is connected with apps.py


def createProfile(sender, instance, created, **kwargs):
    '''
        if user is created then profile will also get created
    '''
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            name=user.first_name,
            username=user.username,
            email=user.email
        )

        subject = 'Welcome to DevSe🔍rch'
        message = f'Hi {profile.name}, we are glad that you are here! lets connect with other developers and find some projects.'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # sender
            [profile.email],  # receiver
            fail_silently=False
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    '''
        if profile is deleted then user will also get deleted,
        if user is deleted then by CASCADING rule profile will also get deleted
    '''
    try:
        user = instance.user
        user.delete()
    except:
        pass


# connects signals to receiver
post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)

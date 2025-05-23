from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, UserProfile


#OTHER WAY OF CONNECTING WITH 'USER' MODEL.
@receiver(post_save, sender=User)
def post_save_create_profile_reciever(sender, instance, created, **kwargs):
    print(created)
    if created:
#HOW DO WE CREATE THE 'USER PROFILE' GIVEN BELOW
        UserProfile.objects.create(user=instance)
        print("User Profile is created")

    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            #CREATE THE USER PROFILE, IF NOT EXIST.
            UserProfile.objects.create(user=instance)
            print("Profile was not existed, but I created one.")

        print("User is Updated")



#WE ARE CONNECTING THIS MODEL WITH USER MODEL.
#post_save.connect(post_save, post_save_create_profile_reciever, sender=User)
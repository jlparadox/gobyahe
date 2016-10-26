from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from versatileimagefield.fields import VersatileImageField
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
import hashlib

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
       return self.name

class Itinerary(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=140)
    location = models.CharField(max_length=140, blank=True, null=True)
    date = models.DateField()
    reservation_deadline = models.DateField()
    tags = models.TextField()
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=6)
    slots = models.IntegerField()
    days_duration = models.PositiveSmallIntegerField(default='1')
    nights_duration = models.PositiveSmallIntegerField(default='1')
    pub_date = models.DateTimeField(auto_now=True)
    isPrivate = models.NullBooleanField()
    isRecurring = models.NullBooleanField()
#   primary_image = VersatileImageField(
#        'Image',
#        upload_to='images/',
#        null=True,
#    )

    def __str__(self):
       return self.name 

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
 
    def __unicode__(self):
        return "{}'s profile".format(self.user.username)
 
    class Meta:
        db_table = 'user_profile'
 
    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False

    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
     
        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)
     
        return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email).hexdigest())

 
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
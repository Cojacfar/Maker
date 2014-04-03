from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User)

	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True, default="/static/images/default_pic.jpg")
	banner = models.ImageField(upload_to='profile_images', blank=True, default="/static/images/default_background.jpg")

	display_name = models.CharField(max_length=50, blank=False)

	def __unicode__(self):
		return self.user.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])



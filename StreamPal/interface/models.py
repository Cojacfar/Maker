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
	relationships = models.ManyToManyField('self', through='Relationship',
		symmetrical=False, related_name='related_to')
	#following = models.ManyToManyField('self', through='Relationship',
	#	symmetrical=False, related_name='related_to')
	#friends = models.ManyToManyField('self', through='Relationship',
	#	symmetrical=False, related_name='related_to')
	
	def add_relationship(self, person, status):
		relationship, created = Relationship.objects.get_or_create(
			from_person=self,
			to_person=person,
			status=status)
		return relationship 

	def remove_relationship(self, person, status):
		Relationship.objects.filter(
			from_person=self,
			to_person=person,
			status=status).delete()
		return

	def get_relationship(self, status):
		return self.relationships.filter(
			from_people__status=status,
			from_people__to_person=self)

	def get_related_to(self, status):
		return self.related_to.filter(
			from_people__status=status,
			from_people__to_person=self)

	def get_following(self):
		return self.get_relationship(1)

	def get_followers(self):
		return self.get_related_to(1)

	def __unicode__(self):
		return self.user.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class Relationship(models.Model):
	from_person = models.ForeignKey(UserProfile, related_name='from_people')
	to_person = models.ForeignKey(UserProfile, related_name='to_people')
	status = models.IntegerField(choices=((0, 'blocked'),(1, 'following')))




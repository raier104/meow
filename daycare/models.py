# from django.db import models

from django.db import models


class Daycare(models.Model):
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=300)
	phone = models.CharField(max_length=20, blank=True)
	description = models.TextField(blank=True)
	image = models.ImageField(upload_to='daycare/', blank=True, null=True)
	map_link = models.URLField(blank=True, null=True)
	facebook_page = models.URLField("Facebook Page", blank=True, null=True)

	def __str__(self):
		return self.name

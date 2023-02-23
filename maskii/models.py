from django.db import models

class FileUpload(models.Model):
	img = models.ImageField(upload_to='images/')

# Create your models here.

from django.db import models

class WebcamImage(models.Model):
    image = models.ImageField(upload_to='webcam_images/')
    timestamp = models.DateTimeField(auto_now_add=True)

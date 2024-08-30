from django.db import models

# Create your models here.
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ProcessedImage(models.Model):
    original_image = models.ImageField(upload_to='uploads/')
    processed_image = models.ImageField(upload_to='processed/')
    upload_time = models.DateTimeField(auto_now_add=True)
    processed_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Original: {self.original_image.name}, Processed: {self.processed_image.name}"

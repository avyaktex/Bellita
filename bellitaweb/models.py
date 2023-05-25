from django.db import models

class Form(models.Model):
    input_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=10)
    date = models.DateField(null=True)
    email = models.EmailField(max_length=255, default='')
    selected_services = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.input_name
    
class Services_by_cat(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=20)
    service_time = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
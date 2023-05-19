from django.db import models

class FormData(models.Model):
    input_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=10)
    date = models.DateField(null=True)
    time = models.CharField(max_length=20)

    def __str__(self):
        return self.input_name

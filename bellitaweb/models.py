from django.db import models

class Form(models.Model):
    input_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=10)
    date = models.DateField(null=True)

    def __str__(self):
        return self.input_name
    
class Service_list(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    service_time = models.TimeField()
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    cat_id = models.IntegerField(primary_key=True)
    cat_name = models.CharField(max_length=255)
    service_qty = models.IntegerField()

    def __str__(self):
        return self.cat_name


class Service(models.Model):
    ser_id = models.IntegerField(primary_key=True)
    ser_name = models.CharField(max_length=255)
    ser_duration = models.IntegerField()
    ser_price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.ser_name
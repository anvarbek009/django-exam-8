from django.db import models

# Create your models here.

class PaymentType(models.Model):
    name = models.CharField(max_length=100)
    image=models.ImageField(upload_to='paymenttypes/', blank=True,null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'payment_types'

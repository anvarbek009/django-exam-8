from django.db import models
from users.models import User
# Create your models here.
class CategoryTransition(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'category_transitions'

class PaymentType(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=100, decimal_places=2,default=0)
    image=models.ImageField(upload_to='paymenttypes/', blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.name} - {self.balance}'
    
    class Meta:
        db_table = 'payment_types'

class CategoryThings(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='category_things/')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'category_things'

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_transition = models.ForeignKey(CategoryTransition, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    date = models.DateField()
    image = models.ImageField(upload_to='transaction/', blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.name} - {self.category_transition.name} - {self.payment_type.name}'
    
    class Meta:
        db_table = 'transactions'



class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.user.name} - Wallet Balance: {self.balance}'
    
    class Meta:
        db_table = 'wallets'


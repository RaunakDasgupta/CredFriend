from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    monthly_salary = models.IntegerField()
    approved_limit=models.IntegerField(null=True, blank=True)
    current_debt=models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    

class Loan(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE,null=True, blank=True)
    loan_id = models.IntegerField(db_index=True)
    amount = models.IntegerField()
    tenure = models.IntegerField()
    interest_rate = models.FloatField()
    monthly_payment=models.FloatField(null=True, blank=True)
    paid_on_time=models.IntegerField(null=True, blank=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)

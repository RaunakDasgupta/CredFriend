from collections.abc import Iterable
from django.db import models
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10,unique=True)
    monthly_salary = models.IntegerField()
    age = models.IntegerField(null=True, blank=True)
    approved_limit=models.IntegerField(null=True, blank=True)
    current_debt=models.IntegerField(null=True, blank=True)
    credit_score=models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def save(self, *args, **kwargs):
        if(self.approved_limit==None):
            self.approved_limit=36*self.monthly_salary
        return super().save()
    

class Loan(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE,null=True, blank=True)
    loan_id = models.AutoField(primary_key=True)
    amount = models.IntegerField()
    tenure = models.IntegerField()
    interest_rate = models.FloatField()
    monthly_payment=models.FloatField(null=True, blank=True)
    paid_on_time=models.IntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     if(self.start_date==None):
    #         self.start_date=datetime.now()
    #     if(self.end_date==None):
    #         self.end_date=self.start_date+relativedelta(months=self.tenure)
    #     return super().save()
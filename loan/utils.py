from django.db import models
import datetime

def calculate_credit_score(customer_instance, customer_loans_instance):
    
    credit_score=0
    no_of_loans=customer_loans_instance.aggregate(models.Count('id'))['id__count'] or 0
    total_tenure=customer_loans_instance.aggregate(models.Sum('tenure'))['tenure__sum'] or 0
    total_paid_on_time=customer_loans_instance.aggregate(models.Sum('paid_on_time'))['paid_on_time__sum'] or 0
    sum_of_current_loans=customer_loans_instance.filter(end_date__gte=datetime.date.today()).aggregate(models.Sum('amount'))['amount__sum'] or 0
    no_of_past_loans=customer_loans_instance.filter(end_date__lt=datetime.date.today()).aggregate(models.Count('id'))['id__count'] or 0
    sum_of_current_year_emi=customer_loans_instance.filter(end_date__gte=datetime.date(datetime.date.today().year, 1, 1)).aggregate(models.Sum('monthly_payment'))['monthly_payment__sum'] or 0

    if(sum_of_current_loans>customer_instance.approved_limit):
        return credit_score
    
    w1=0.2
    w2=0.2
    w3=0.3
    w4=0.3

    s1=(total_paid_on_time/total_tenure)*w1
    s2=(no_of_past_loans/no_of_loans)*w2
    s3=(1-((2*sum_of_current_year_emi)/customer_instance.monthly_salary))*w3
    s4=(1-(sum_of_current_loans/customer_instance.approved_limit))*w4

    credit_score=(s1+s2+s3+s4)*100

    
    return credit_score
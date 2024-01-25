from django.db import models
import datetime

# Function to calculate credit score
def calculate_credit_score(customer_instance, customer_loans_instance):
    
    credit_score=0
    
    #Total number of loans taken by the customer
    no_of_loans=customer_loans_instance.aggregate(models.Count('loan_id'))['loan_id__count'] or 0
    
    #Total tenure of all loans taken by the customer
    total_tenure=customer_loans_instance.aggregate(models.Sum('tenure'))['tenure__sum'] or 0
    
    #Total number of loans paid on time by the customer
    total_paid_on_time=customer_loans_instance.aggregate(models.Sum('paid_on_time'))['paid_on_time__sum'] or 0
    
    #Total sum of current loans taken by the customer
    sum_of_current_loans=customer_loans_instance.filter(end_date__gte=datetime.date.today()).aggregate(models.Sum('amount'))['amount__sum'] or 0
    
    #Total number of past loans taken by the customer
    no_of_past_loans=customer_loans_instance.filter(end_date__lt=datetime.date.today()).aggregate(models.Count('loan_id'))['loan_id__count'] or 0
    
    #Total sum of current EMIs of the customer
    sum_of_current_emi=customer_loans_instance.filter(end_date__gte=datetime.date.today()).aggregate(models.Sum('monthly_payment'))['monthly_payment__sum'] or 0
    
    #Total sum of EMIs of the customer for the current year
    sum_of_current_year_emi=customer_loans_instance.filter(end_date__gte=datetime.date(datetime.date.today().year, 1, 1)).aggregate(models.Sum('monthly_payment'))['monthly_payment__sum'] or 0

    #Condition to check if the current loans are more than the approved limit for the customer
    if(sum_of_current_loans>customer_instance.approved_limit):
        return credit_score
    
    #Condition to check if the sum of current EMIs are more than 50% of the monthly salary of the customer
    if((2*sum_of_current_emi)>customer_instance.monthly_salary):
        return credit_score

    
    #Weight for total emis paid on time
    w1=0.2
    
    #Weight for total number of past loans
    w2=0.2
    
    #Weight for total sum of current year EMIs
    w3=0.3
    
    #Weight for total sum of current loans
    w4=0.3

    #Scores for each of the parameters
    s1=(total_paid_on_time/total_tenure)*w1
    s2=(no_of_past_loans/no_of_loans)*w2
    s3=(1-((2*sum_of_current_year_emi)/customer_instance.monthly_salary))*w3
    s4=(1-(sum_of_current_loans/customer_instance.approved_limit))*w4

    #Total credit score out of 100
    credit_score=(s1+s2+s3+s4)*100

    return credit_score


def check_loan_approval(customer_instance, customer_loans_instance):
    
    #Total sum of current loans taken by the customer
    sum_of_current_loans=customer_loans_instance.filter(end_date__gte=datetime.date.today()).aggregate(models.Sum('amount'))['amount__sum'] or 0
    
    #Condition to check if the current loans are more than the approved limit for the customer
    if(sum_of_current_loans>customer_instance.approved_limit):
        return False
    
    return True
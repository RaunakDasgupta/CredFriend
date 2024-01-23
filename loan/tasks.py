import base64

import pandas as pd

from .models import Customer, Loan
from celery import Celery

app = Celery('tasks')


@app.task
def add_customer(excel_file_base64):
    excel_file = base64.b64decode(excel_file_base64)
    df = pd.read_excel(excel_file)
    for rows in df.iterrows():
        row = rows[1]
        customer = Customer.objects.get_or_create(
            first_name=row['First Name'],
            last_name=row['Last Name'],
            phone_number=row['Phone Number'],
            monthly_salary=row['Monthly Salary'],
            approved_limit=row['Approved Limit'],
        )

@app.task
def add_loan(excel_file_base64):
    excel_file = base64.b64decode(excel_file_base64)
    df = pd.read_excel(excel_file)
    for rows in df.iterrows():
        row = rows[1]
        try:
            loan = Loan.objects.get_or_create(
                customer_id=row['Customer ID'],
                loan_id=row['Loan ID'],
                amount=row['Loan Amount'],
                tenure=row['Tenure'],
                interest_rate=row['Interest Rate'],
                monthly_payment=row['Monthly payment'],
                paid_on_time=row['EMIs paid on Time'],
                start_date=row['Date of Approval'],
                end_date=row['End Date']
            )
        except:
            pass
        


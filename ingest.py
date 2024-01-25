import base64
import os
import django
import pandas as pd
# Set the DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Setup Django
django.setup()

from loan.models import Customer, Loan



def add_customer(excel_file_base64):
    excel_file = base64.b64decode(excel_file_base64)
    df = pd.read_excel(excel_file)
    for rows in df.iterrows():
        row = rows[1]
        customer, created= Customer.objects.get_or_create(
            first_name=row['First Name'],
            last_name=row['Last Name'],
            phone_number=row['Phone Number'],
            monthly_salary=row['Monthly Salary'],
            approved_limit=row['Approved Limit'],
        )
        customer.age=row['Age']
        customer.save()

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
        

def customer_function():
    with open("customer_data.xlsx", 'rb') as file: 
        excel_raw_bytes = file.read()
        excel_base64 = base64.b64encode(excel_raw_bytes).decode()
    add_customer(excel_base64)

    return "Successfully ingested"

def loan_function():
    with open("loan_data.xlsx", 'rb') as file: 
        excel_raw_bytes = file.read()
        excel_base64 = base64.b64encode(excel_raw_bytes).decode()
    add_loan(excel_base64)

    return "Successfully ingested"


if __name__ == "__main__":
    customer_function()
    loan_function()
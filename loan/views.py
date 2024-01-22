# myapp/views.py
import base64

from .tasks import add_customer, add_loan

# myapp/views.py
from django.shortcuts import render
from django.http import JsonResponse

def my_function_view(request):
    # Your function logic goes here
    customer_data = customer_function()  # Replace with your actual function
    loan_data = loan_function()  # Replace with your actual function
    # Return a JSON response
    return JsonResponse(
        {"customer_data": customer_data,
        "loan_data": loan_data,})


def customer_function():
    with open("customer_data.xlsx", 'rb') as file: 
        excel_raw_bytes = file.read()
        excel_base64 = base64.b64encode(excel_raw_bytes).decode()
    add_customer(excel_base64)

    return "Function executed successfully"

def loan_function():
    with open("loan_data.xlsx", 'rb') as file: 
        excel_raw_bytes = file.read()
        excel_base64 = base64.b64encode(excel_raw_bytes).decode()
    add_loan(excel_base64)

    return "Function executed successfully"



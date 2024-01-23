
import base64

from rest_framework.decorators import api_view
from .tasks import add_customer, add_loan


from django.shortcuts import render
from django.http import JsonResponse

@api_view(['GET'])
def ingest_data(request):
    # Your function logic goes here
    customer_data = customer_function()
    loan_data = loan_function()  
    return JsonResponse(
        {"customer_data": customer_data,
        "loan_data": loan_data,})


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


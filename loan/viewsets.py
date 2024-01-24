from rest_framework import views
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import models
from rest_framework import generics

from .utils import calculate_credit_score, check_loan_approval
from .models import Loan, Customer
from rest_framework import serializers


from .serializers import LoanSerializer, CreateLoanSerializer, CustomerSerializer, CreateCustomerSerializer, CheckEligibilitySerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CreateCustomerSerializer

    allowed_methods = ['POST']

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        if(serializer.is_valid()):
            customer=serializer.save()
            print(customer)
            response_data=CustomerSerializer(customer).data
            return Response(response_data, status=201)

    def list(self, request, *args, **kwargs):
        return Response({"message": "Not allowed"}, status=405)
    
class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @action(detail=False, methods=['GET'], url_path='view-loan/(?P<loan_id>\d+)')
    def view_loan(self, request, loan_id=None):
        loan_instance = Loan.objects.get(loan_id=loan_id)
        response_data = self.serializer_class(loan_instance).data
        return Response(response_data, status=200)

    @action(detail=False, methods=['GET'], url_path='view-loans/(?P<customer_id>\d+)')
    def view_loans_by_customer(self, request, customer_id=None):
        loans = Loan.objects.filter(customer_id=customer_id)
        serializer = self.serializer_class(loans, many=True)
        return Response(serializer.data, status=200)




class CreateLoanView(views.APIView):
    serializer_class = CreateLoanSerializer

    def post(self, request, *args, **kwargs):
        
            serializer=self.serializer_class(data=request.data)
            if(serializer.is_valid()):
            
                customer_id = serializer._validated_data['customer_id']
                amount = serializer._validated_data['amount']
                interest_rate = serializer._validated_data['interest_rate']
                tenure = serializer._validated_data['tenure']

                corrected_interest_rate = interest_rate
                customer=Customer.objects.get(id=customer_id)
                customer_loans=Loan.objects.filter(customer_id=customer_id)

                if(customer.credit_score==None):
                    customer.credit_score=calculate_credit_score(customer, customer_loans)
                    customer.save()

                loan_approval=check_loan_approval(customer, customer_loans)
                if(customer.credit_score>50):
                    corrected_interest_rate=8
                elif(customer.credit_score>30 and customer.credit_score<50):
                    corrected_interest_rate=12
                elif(customer.credit_score>10 and customer.credit_score<30):
                    corrected_interest_rate=16
                elif(loan_approval==False):
                    return Response({"Approval": "Denied",
                                    'message': 'Loan not approved due to high current debt'})
                
                else:
                    return Response({"Approval": "Denied",
                                    'message': 'Loan not approved due to low credit score'})
                
                loan_instance=Loan.objects.create(customer_id=customer_id, amount=amount, interest_rate=interest_rate, tenure=tenure)
                return Response({'customer_id': customer_id,
                                'loan_id': loan_instance.loan_id,
                                'Approval': 'Approved',  
                                'tenure': tenure,
                                'monthly_payment': amount*(1+corrected_interest_rate/100)/tenure
                                }
                                )
            else:
                return Response(serializer.errors, status=400)


class CheckEligibilityView(views.APIView):
    serializer_class = CheckEligibilitySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if(serializer.is_valid()):
            customer_id = serializer.validated_data['customer_id']
            loan_amount = serializer.validated_data['loan_amount']
            interest_rate = serializer.validated_data['interest_rate']
            tenure = serializer.validated_data['tenure']

            corrected_interest_rate = interest_rate
            customer=Customer.objects.get(id=customer_id.id)
            customer_loans=Loan.objects.filter(customer_id=customer_id.id)

            customer.credit_score=calculate_credit_score(customer, customer_loans)
            customer.save()

            if(customer.credit_score>50):
                corrected_interest_rate=8
            elif(customer.credit_score>30 and customer.credit_score<50):
                corrected_interest_rate=12
            elif(customer.credit_score>10 and customer.credit_score<30):
                corrected_interest_rate=16
            else:
                return Response({"Approval": "Denied"})
            
            return Response({'customer_id': customer_id.id,
                             'Approval': 'Approved',  
                            'interest_rate': interest_rate, 
                            'corrected_interest_rate':corrected_interest_rate,
                            'tenure': tenure,
                            'monthly_payment': loan_amount*float((1+corrected_interest_rate/100)/tenure)
                            }
                            )
        else:
            return Response(serializer.errors, status=400)
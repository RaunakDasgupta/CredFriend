from rest_framework import views
from rest_framework import viewsets
from rest_framework.response import Response

from .utils import calculate_credit_score
from .models import Loan, Customer
from rest_framework import serializers


from .serializers import LoanSerializer, CustomerSerializer, CheckEligibilitySerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    allowed_methods = ['POST']

    def list(self, request, *args, **kwargs):
        return Response({"message": "Not allowed"}, status=405)
    


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
                            'tenure': tenure, 'monthly_payment': customer.monthly_salary,
                            'monthly_payment': loan_amount*(1+corrected_interest_rate/100)/tenure
                            }
                            )
        else:
            return Response(serializer.errors, status=400)
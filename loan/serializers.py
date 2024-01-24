from rest_framework import serializers


from .models import Loan, Customer
from loan import models

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = 'first_name', 'last_name', 'age','monthly_salary', 'phone_number', 'approved_limit'

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)

class CreateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = 'first_name', 'last_name', 'age','monthly_salary', 'phone_number'

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)
    

class CreateLoanSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure = serializers.FloatField()

    def validate(self, attrs):
        customer_instance = Customer.objects.get(id=attrs['customer_id'])
        if attrs['amount'] > customer_instance.approved_limit:
            raise serializers.ValidationError("Loan amount is greater than approved limit")
        return super().validate(attrs)

    def create(self, validated_data):
        loan_instance = Loan.objects.create(**validated_data)
        return loan_instance
            


class CheckEligibilitySerializer(serializers.Serializer):
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    loan_amount = serializers.IntegerField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()

    def validate(self, attrs):
        if attrs['loan_amount'] > attrs['customer_id'].approved_limit:
            raise serializers.ValidationError("Loan amount is greater than approved limit")
        return super().validate(attrs)

    def create(self, validated_data):
        return super().create(validated_data)
from rest_framework import serializers

from .models import Loan, Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

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
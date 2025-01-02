from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount', 'status', 'transaction_id', 'patient', 'payment_date']

    def create(self, validated_data):
        return Payment.objects.create(**validated_data)

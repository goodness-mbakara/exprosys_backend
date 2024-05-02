from rest_framework import serializers
from ..models import Customer, Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['date', 'invoice_number', 'transaction_type', 'amount']

class CustomerSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'

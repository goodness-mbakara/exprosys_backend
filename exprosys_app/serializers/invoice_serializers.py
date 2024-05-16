from rest_framework import serializers

from ..models import  PostExportInvoice,  InvoicePostingReport, PostPayment

class PostExportInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostExportInvoice
        fields = '__all__'

class InvoicePostingReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoicePostingReport
        fields = '__all__'


class PostPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostPayment
        fields = '__all__'
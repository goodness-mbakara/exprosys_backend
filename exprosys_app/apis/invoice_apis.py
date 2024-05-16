from rest_framework import generics
from ..models import  PostExportInvoice, InvoicePostingReport, PostPayment
from ..serializers.invoice_serializers import  PostExportInvoiceSerializer, PostPaymentSerializer, InvoicePostingReportSerializer


class PostExportInvoiceCreateView(generics.CreateAPIView):
    queryset = PostExportInvoice.objects.all()
    serializer_class = PostExportInvoiceSerializer

class InvoicePostingReportDetailView(generics.RetrieveAPIView):
    queryset = InvoicePostingReport.objects.all()
    serializer_class = InvoicePostingReportSerializer

class PostPaymentCreateView(generics.CreateAPIView):
    queryset = PostPayment.objects.all()
    serializer_class = PostPaymentSerializer
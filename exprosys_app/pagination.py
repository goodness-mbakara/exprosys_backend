from rest_framework.pagination import PageNumberPagination

class ExporterPagination(PageNumberPagination):
    page_size = 17
    page_size_query_param = 'page_size'
    max_page_size = 100

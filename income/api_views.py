from unicodedata import category
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from income.serializers import IncomeSerializer
from income.models import Income
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated 


class IncomePagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class IncomeList(ListAPIView):
    permission_classes = (IsAuthenticated,) 
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('date', 'category')
    search_fields = ('category', 'description')
    pagination_class = IncomePagination


class IncomeCreate(CreateAPIView):
    permission_classes = (IsAuthenticated,) 
    serializer_class = IncomeSerializer

    def create(self, request, *args, **kwargs):
        try:
            amount = request.data.get('amount')
            if amount is not None and float(amount) <= 0.0:
                raise ValidationError({'amount': 'Must be above £0.00'})
        except ValueError:
            raise ValidationError({'amount': 'Amount has to be a number'})
        return super().create(request, *args, **kwargs)


class IncomeRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,) 
    queryset = Income.objects.all()
    lookup_field = 'id'
    serializer_class = IncomeSerializer
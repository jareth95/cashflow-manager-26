from unicodedata import category
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from expenses.serializers import ExpenseSerializer
from expenses.models import Expense
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated 


class ExpensesPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class ExpenseList(ListAPIView):
    permission_classes = (IsAuthenticated,) 
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('date', 'category')
    search_fields = ('category', 'description')
    pagination_class = ExpensesPagination


class ExpenseCreate(CreateAPIView):
    serializer_class = ExpenseSerializer

    def create(self, request, *args, **kwargs):
        try:
            amount = request.data.get('amount')
            if amount is not None and float(amount) <= 0.0:
                raise ValidationError({'amount': 'Must be above £0.00'})
        except ValueError:
            raise ValidationError({'amount': 'Amount has to be a number'})
        return super().create(request, *args, **kwargs)


class ExpenseRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    lookup_field = 'id'
    serializer_class = ExpenseSerializer
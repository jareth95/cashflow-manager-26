from unicodedata import category
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from expenses.serializers import ExpenseSerializer
from expenses.models import Expense
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


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
    permission_classes = (IsAuthenticated,) 
    serializer_class = ExpenseSerializer

    def create(self, request, *args, **kwargs):
        expense_data = request.data
        user = Token.objects.get(key=expense_data['owner']).user
        print(expense_data)
        new_expense = Expense.objects.create(
            owner=user,
            amount=expense_data['amount'],
            category=expense_data['category'],
            date=expense_data['date'],
            description=expense_data['description']
        ).save()

        serializer = ExpenseSerializer(new_expense)
        return Response(serializer.data)


class ExpenseRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,) 
    queryset = Expense.objects.all()
    lookup_field = 'id'
    serializer_class = ExpenseSerializer
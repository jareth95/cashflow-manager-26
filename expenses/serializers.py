from rest_framework import serializers
from expenses.models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('id', 'owner', 'amount', 'category', 'date', 'description')

    
    def to_representation(self, instance):
        return super().to_representation(instance)

    

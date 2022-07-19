from rest_framework import serializers
from .models import Income


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ('id', 'owner', 'amount', 'category', 'date', 'description')

    
    def to_representation(self, instance):
        return super().to_representation(instance)

    

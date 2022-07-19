from unicodedata import name
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='investments'),
    path('add-investment', views.add_investment, name='add-investment'),
    path('investment-delete/<int:id>', views.investment_delete, name='investment-delete'),
    path('investment-edit/<int:id>', views.investment_edit, name='investment-edit'),
    path('search-investment', csrf_exempt(views.search_investment), name='search-investment')
]
from unicodedata import name
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from . import api_views

urlpatterns = [
    path('', views.index, name='income'),
    path('add-income', views.add_income, name='add-income'),
    path('add-source', views.add_source, name='add-source'),
    path('delete-source', views.delete_source, name='delete-source'),
    path('income-edit/<int:id>', views.income_edit, name='income-edit'),
    path('income-delete/<int:id>', views.income_delete, name='income-delete'),
    path('search-income', csrf_exempt(views.search_income), name='search-income'),
    path('income/api/v1/', api_views.IncomeList.as_view()),
    path('income/api/v1/new/', api_views.IncomeCreate.as_view()),
    path('income/api/v1/<int:id>/', api_views.IncomeRetrieveUpdateDestroy.as_view())
]
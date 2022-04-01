from unicodedata import name
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expense', views.add_expense, name='add-expense'),
    path('add-category', views.add_category, name='add-category'),
    path('delete-category', views.delete_category, name='delete-category'),
    path('expense-edit/<int:id>', views.expense_edit, name='expense-edit'),
    path('expense-delete/<int:id>', views.expense_delete, name='expense-delete'),
    path('search-expenses', csrf_exempt(views.search_expenses), name='search-expenses'),
    path('expense_category_summary/<int:year>/<int:month>', views.expense_category_summary, name='expense_category_summary'),
    path('income_category_summary/<int:year>/<int:month>', views.income_category_summary, name='income_category_summary'),
    path('stats', views.stats_view, name='stats')
]
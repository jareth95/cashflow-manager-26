from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('current_portfolio', views.current_portfolio, name='current_portfolio'),
    path('current_expenses', views.current_expenses, name='current_expenses'),
    path('curent_income', views.curent_income, name='curent_income')
]
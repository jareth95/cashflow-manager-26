from telnetlib import AUTHENTICATION
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferances.models import UserPreference
import datetime
from income.models import Income
from django.db.models.functions import ExtractYear



@login_required(login_url='/authentication/login')
def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(date__istartswith=search_str, owner=request.user) | Expense.objects.filter(description__icontains=search_str, owner=request.user) | Expense.objects.filter(category__icontains=search_str, owner=request.user)

        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    expenses = Expense.objects.filter(owner=request.user).order_by('-date')
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    if currency:
        user_preferences = UserPreference.objects.get(user=request.user).currency

    context = {
        'expenses':expenses,
        'page_obj':page_obj,
        'currency': user_preferences,
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/authentication/login')
def add_category(request):

    if request.method == 'POST':
        name = request.POST['name']

        if not name:
            messages.error(request, 'Name is required')
            return render(request, 'expenses/add_category.html')
        
        Category.objects.create(
            name=name,
            owner=request.user,
        ).save()

        messages.success(request, 'Category saved')
        return redirect('expenses')

    return render(request, 'expenses/add_category.html')


@login_required(login_url='/authentication/login')
def delete_category(request):
    categories = Category.objects.filter(owner=request.user)

    context = {
        'categories':categories,
    }

    if request.method == 'POST':
        chosen_category = request.POST['category']
        category = Category.objects.get(name=chosen_category)
        category.delete()

        messages.success(request, 'Category deleted')
        return redirect('expenses')

    return render(request, 'expenses/delete_category.html', context)


@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.filter(owner=request.user)

    context = {
        'categories':categories,
        'values': request.POST
    }

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        expense_date = request.POST['expense_date']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        elif not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', context)
        elif not category:
            messages.error(request, 'Category is required')
            return render(request, 'expenses/add_expense.html', context)
        elif not expense_date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/add_expense.html', context)
        
        Expense.objects.create(
            amount=amount,
            date=expense_date,
            category=category,
            description=description,
            owner=request.user
        ).save()

        messages.success(request, 'Expense saved')
        return redirect('expenses')

    return render(request, 'expenses/add_expense.html', context)


@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.filter(owner=request.user)
    context = {
        'expense':expense,
        'values':expense,
        'categories':categories
    }

    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        expense_date = request.POST['expense_date']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        elif not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/edit-expense.html', context)
        elif not category:
            messages.error(request, 'Category is required')
            return render(request, 'expenses/edit-expense.html', context)
        elif not expense_date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/edit-expense.html', context)

        expense.amount = amount
        expense.date = expense_date
        expense.category = category
        expense.description = description
        expense.owner = request.user
        expense.save()

        messages.success(request, 'Expense updated')
        return redirect('expenses')


@login_required(login_url='/authentication/login')
def expense_delete(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()

    messages.success(request, 'Expense deleted')
    return redirect('expenses')


@login_required(login_url='/authentication/login')
def expense_category_summary(request, year, month):
    expenses = Expense.objects.filter(owner=request.user, date__year=year, date__month=month)
    finalrep = {}

    def get_category(expense):
        return expense.category

    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


@login_required(login_url='/authentication/login')
def income_category_summary(request, year, month):
    income = Income.objects.filter(owner=request.user, date__year=year, date__month=month)
    finalrep = {}

    def get_source(income):
        return income.source

    category_list = list(set(map(get_source, income)))

    def get_expense_source_amount(source):
        amount = 0
        filtered_by_source = income.filter(source=source)

        for item in filtered_by_source:
            amount += item.amount
        return amount

    for x in income:
        for y in category_list:
            finalrep[y] = get_expense_source_amount(y)

    return JsonResponse({'income_category_data': finalrep}, safe=False)


@login_required(login_url='/authentication/login')
def stats_view(request):
    expense_dates = Expense.objects.filter(owner=request.user).dates('date', 'year')
    income_dates = Income.objects.filter(owner=request.user).dates('date', 'year')

    expense_years = [date.year for date in expense_dates]
    income_years = [date.year for date in income_dates]

    in_first = set(expense_years)
    in_second = set(income_years)

    in_second_but_not_in_first = in_second - in_first

    years = expense_years + list(in_second_but_not_in_first)
    years.sort()

    print(years)

    return render(request, 'expenses/stats.html', {'years':years})

    

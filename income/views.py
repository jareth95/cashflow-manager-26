from telnetlib import AUTHENTICATION
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Source, Income
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferances.models import UserPreference



@login_required(login_url='/authentication/login')
def index(request):
    income = Income.objects.filter(owner=request.user).order_by('-date')
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    #currency = UserPreference.objects.get(user=request.user).currency

    context = {
        'income':income,
        'page_obj':page_obj,
        #'currency': currency
    }
    return render(request, 'income/index.html', context)


@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.filter(owner=request.user)

    context = {
        'sources':sources,
        'values': request.POST
    }

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['income_date']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)
        elif not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context)
        elif not source:
            messages.error(request, 'Source is required')
            return render(request, 'income/add_income.html', context)
        elif not date:
            messages.error(request, 'Date is required')
            return render(request, 'income/add_income.html', context)
        
        Income.objects.create(
            amount=amount,
            date=date,
            source=source,
            description=description,
            owner=request.user
        ).save()

        messages.success(request, 'Income saved')
        return redirect('income')

    return render(request, 'income/add_income.html', context)


@login_required(login_url='/authentication/login')
def income_edit(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.filter(owner=request.user)
    context = {
        'income':income,
        'values':income,
        'sources':sources
    }

    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        income_date = request.POST['income_date']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_income.html', context)
        elif not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/edit_income.html', context)
        elif not source:
            messages.error(request, 'Source is required')
            return render(request, 'income/edit_income.html', context)
        elif not income_date:
            messages.error(request, 'Date is required')
            return render(request, 'income/edit_income.html', context)

        income.amount = amount
        income.date = income_date
        income.source = source
        income.description = description
        income.owner = request.user
        income.save()

        messages.success(request, 'Income updated')
        return redirect('income')


@login_required(login_url='/authentication/login')
def income_delete(request, id):
    income = Income.objects.get(pk=id)
    income.delete()

    messages.success(request, 'Income deleted')
    return redirect('income')


@login_required(login_url='/authentication/login')
def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        income = Income.objects.filter(amount__istartswith=search_str, owner=request.user) | Income.objects.filter(date__istartswith=search_str, owner=request.user) | Income.objects.filter(description__icontains=search_str, owner=request.user) | Income.objects.filter(source__icontains=search_str, owner=request.user)

        data = income.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def add_source(request):

    if request.method == 'POST':
        name = request.POST['name']

        if not name:
            messages.error(request, 'Name is required')
            return render(request, 'expenses/add_source.html')
        
        Source.objects.create(
            name=name,
            owner=request.user,
        ).save()

        messages.success(request, 'Souce saved')
        return redirect('income')

    return render(request, 'income/add_source.html')


@login_required(login_url='/authentication/login')
def delete_source(request):
    sources = Source.objects.filter(owner=request.user)

    context = {
        'sources':sources,
    }

    if request.method == 'POST':
        chosen_source = request.POST['source']
        source = Source.objects.get(name=chosen_source)
        source.delete()

        messages.success(request, 'Source deleted')
        return redirect('income')

    return render(request, 'income/delete_source.html', context)



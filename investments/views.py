import imp
from telnetlib import AUTHENTICATION
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferances.models import UserPreference
from .models import Investment
from binance.client import Client
import requests


@login_required(login_url='/authentication/login')
def index(request):
    investments = Investment.objects.filter(owner=request.user).order_by('-buy_date')
    paginator = Paginator(investments, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
   # currency = UserPreference.objects.get(user=request.user).currency

    context = {
        'investment':investments,
        'page_obj':page_obj,
   #     'currency': currency
    }
    return render(request, 'investments/index.html', context)


@login_required(login_url='/authentication/login')
def add_investment(request):

    symbols = "https://api.kraken.com/0/public/AssetPairs"
    symbols = requests.get(symbols)
    symbols = symbols.json()
    tickers = []
    for symbol in symbols['result']:
        
        if str(symbol)[-3:] == 'GBP' or str(symbol)[-3:] == 'EUR' or str(symbol)[-3:] == 'USD':
            tickers.append(symbol)

    context = {
        'tickers': tickers,
        'values': request.POST
    }

    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        exchange = request.POST['exchange']
        buy_price = request.POST['buy_price']
        buy_date = request.POST['buy_date']
        sell_price = request.POST['sell_price']
        sell_date = request.POST['sell_date']
        pnl = 00

        # if name:
        #     api_key = "xxx"
        #     api_secret = "xxx"

        #     client = Client(api_key, api_secret)
        #     exchange_info = client.get_exchange_info()
        #     correct = False
        #     for s in exchange_info['symbols']:
        #         print(s['symbol'])
        #         if name == s['symbol']:
        #             correct = True
        #             break
        #     if not correct:
        #         messages.error(request, 'name not a valid symbol')
        #         return render(request, 'investments/add_investment.html', context)    

        if not name:
            messages.error(request, 'name is required')
            return render(request, 'investments/add_investment.html', context)
        elif not amount:
            messages.error(request, 'amount is required')
            return render(request, 'investments/add_investment.html', context)
        elif not exchange:
            messages.error(request, 'exchange is required')
            return render(request, 'investments/add_investment.html', context)
        elif not buy_price:
            messages.error(request, 'buy price is required')
            return render(request, 'investments/add_investment.html', context)
        elif not buy_date:
            messages.error(request, 'buy date is required')
            return render(request, 'investments/add_investment.html', context)
        elif not sell_price or not sell_date:
            Investment.objects.create(
            name=name,
            amount=amount,
            exchange=exchange,
            buy_price=buy_price,
            buy_date=buy_date,
            owner=request.user
            ).save()
            messages.success(request, 'Investment saved')
            return redirect('investments')
        elif sell_date and sell_price:
            buy_value = int(buy_price) * int(amount)
            sell_value = int(sell_price) * int(amount)
            pnl = sell_value - buy_value
        
        Investment.objects.create(
            name=name,
            amount=amount,
            exchange=exchange,
            buy_price=buy_price,
            buy_date=buy_date,
            sell_price=sell_price,
            sell_date=sell_date,
            pnl=pnl,
            owner=request.user
        ).save()

        messages.success(request, 'Investment saved')
        return redirect('investments')

    return render(request, 'investments/add_investment.html', context)


@login_required(login_url='/authentication/login')
def investment_delete(request, id):
    investment = Investment.objects.get(pk=id)
    investment.delete()

    messages.success(request, 'Investment deleted')
    return redirect('investments')


@login_required(login_url='/authentication/login')
def investment_edit(request, id):
    investment = Investment.objects.get(pk=id)
    context = {
        'investment':investment,
        'values':investment,
    }

    if request.method == 'GET':
        return render(request, 'investments/edit_investment.html', context)

    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        exchange = request.POST['exchange']
        buy_price = request.POST['buy_price']
        buy_date = request.POST['buy_date']
        sell_price = request.POST['sell_price']
        sell_date = request.POST['sell_date']

        if not name:
            messages.error(request, 'name is required')
            return render(request, 'investments/edit_investment.html', context)
        elif not amount:
            messages.error(request, 'amount is required')
            return render(request, 'investments/edit_investment.html', context)
        elif not exchange:
            messages.error(request, 'exchange is required')
            return render(request, 'investments/edit_investment.html', context)
        elif not buy_price:
            messages.error(request, 'buy price is required')
            return render(request, 'investments/edit_investment.html', context)
        elif not buy_date:
            messages.error(request, 'buy date is required')
            return render(request, 'investments/edit_investment.html', context)

        investment.name = name
        investment.amount = amount
        investment.exchange = exchange
        investment.buy_price = buy_price
        investment.buy_date = buy_date
        if sell_price:
            investment.sell_price = sell_price
        if sell_date:
            investment.sell_date = sell_date
        investment.owner = request.user
        investment.save()

        messages.success(request, 'Investment updated')
        return redirect('investments')


@login_required(login_url='/authentication/login')
def search_investment(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        investments = Investment.objects.filter(name__istartswith=search_str, owner=request.user) | Investment.objects.filter(amount__istartswith=search_str, owner=request.user) | Investment.objects.filter(sell_price__istartswith=search_str, owner=request.user) | Investment.objects.filter(buy_price__istartswith=search_str, owner=request.user) | Investment.objects.filter(sell_date__istartswith=search_str, owner=request.user) | Investment.objects.filter(buy_date__istartswith=search_str, owner=request.user) | Investment.objects.filter(buy_price__icontains=search_str, owner=request.user) | Investment.objects.filter(exchange__icontains=search_str, owner=request.user)

        data = investments.values()
        return JsonResponse(list(data), safe=False)

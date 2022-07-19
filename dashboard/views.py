from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
from investments.models import Investment
import datetime
from income.models import Income
from expenses.models import Expense
from currency_converter import CurrencyConverter
from django.http import JsonResponse

@login_required(login_url='/authentication/login')
def index(request):
   
    context = {
        
    }
    return render(request, 'dashboard/index.html', context)


def current_portfolio(request):
    open_investments = Investment.objects.filter(owner=request.user, sell_price__isnull=True)
    positions = []
    for investment in open_investments:
            open = get_crypto_price(investment.name, investment.amount)
            if not positions:
                positions.append(open)
            else:
                for position in positions:
                    if investment.name not in position['symbol']:
                        positions.append(open)
                    else:
                        position['amount'] += open['amount']
    symbols = []
    prices = []
    amount = []
    for symbol in positions:
        symbols.append(symbol['symbol'])
        prices.append(str(symbol['price']))
        amount.append(str(symbol['amount']))
    positions = {
        'symbols': symbols,
        'prices': prices,
        'amount': amount
    }
    return JsonResponse({'positions': positions}, safe=False)


def get_crypto_price(symbol, amount):
    url = f" https://api.kraken.com/0/public/Ticker?pair={symbol}"
    data = requests.get(url)  
    data = data.json()
    key = list(data['result'].keys())[0]
    if key[-3:] != 'GBP':
        c = CurrencyConverter()
        price = c.convert(data['result'][key]['a'][0], key[-3:], 'GBP')
    else:
        price = data['result'][key]['a'][0]
    
    return {
        'symbol': symbol,
        'price': price,
        'amount': amount
    }


def curent_income(request):
    today = datetime.date.today()
    incomes = Income.objects.filter(owner=request.user, date__month=today.month)
    names = []
    amounts = []
    for income in incomes:
        name = income.source
        amount = income.amount
        if name not in names:
            names.append(name)
            amounts.append(amount)
        else:
            for index, already_named in enumerate(names):
                if name == already_named:
                    amounts[index] += amount

    incomes = {
        'names': names,
        'amounts': amounts
    }
    return JsonResponse({'incomes': incomes}, safe=False)


def current_expenses(request):
    today = datetime.date.today()
    expenses = Expense.objects.filter(owner=request.user, date__month=today.month)
    names = []
    amounts = []
    for expense in expenses:
        name = expense.category
        amount = expense.amount
        if name not in names:
            names.append(name)
            amounts.append(amount)
        else:
            for index, already_named in enumerate(names):
                if name == already_named:
                    amounts[index] += amount

    expenses = {
        'names': names,
        'amounts': amounts
    }
    return JsonResponse({'expenses': expenses}, safe=False)


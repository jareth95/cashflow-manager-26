from django.shortcuts import render,redirect
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required(login_url='/authentication/login')
def index(request):
    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)
    
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path) as json_file:
        data = json.load(json_file)
        for k,v in data.items():
            currency_data.append({'name':k, 'value':v})

    if request.method == 'POST':
    
        currency = request.POST['currency']
        if exists:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Currency saved')

    return render(request, 'preferences/index.html', {'currencies':currency_data, 'user_preferences':user_preferences})


@login_required(login_url='/authentication/login')
def change_password(request):

    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'preferences/change_password.html')

        if len(password) < 6:
            messages.error(request, 'Password is too short')
            return render(request, 'preferences/change_password.html')
        try:
            user = request.user
            user.set_password(password)
            user.save()

            messages.success(request, 'Password changed successfully')
            return redirect('preferences')

        except Exception as identifier:
                messages.info(request, 'Something went wrong, try again')
                return render(request, 'preferences/change_password.html')

    return render(request, 'preferences/change_password.html')
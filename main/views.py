import datetime
from django.shortcuts import render, redirect, get_object_or_404
from main import models
from main import forms
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse("main:login"))
    response.delete_cookie('last_login')
    return response

def delete_product(request, id):
    product_detail = get_object_or_404(models.Product, pk=id)
    product_detail.delete()
    return HttpResponseRedirect(reverse('main:display'))

def edit_product(request, id):
    product_detail = get_object_or_404(models.Product, pk=id)
    formz = forms.ProductForm(request.POST or None, instance=product_detail)
    if request.method == "POST" and formz.is_valid():
            formz.save()
            return redirect('main:product_detail', id=id)

    return render(request, "edit.html", {'form': formz})

def login_user(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:display"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, 'Please fill out the form correctly.')

    form.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter username'})
    form.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
    return render(request, 'login.html', {'form': form})

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account successfully created!')
            return redirect('main:login')
        else:
            messages.error(request, 'Please fill out the form correctly.')
    
    for field in form.fields.values():
        field.widget.attrs.update({'class': 'form-control'})
        
    return render(request, 'register.html', {'form': form})

def show_xml(request):
    products = models.Product.objects.all()
    data = serializers.serialize("xml", products)
    return HttpResponse(data, content_type="application/xml")

def show_json(request):
    products = models.Product.objects.all()
    data = serializers.serialize("json", products)
    return HttpResponse(data, content_type="application/json")

def xml_by_id(request, id):
    product = get_object_or_404(models.Product, pk=id)
    data = serializers.serialize("xml", [product])
    return HttpResponse(data, content_type="application/xml")

def json_by_id(request, id):
    product = get_object_or_404(models.Product, pk=id)
    data = serializers.serialize("json", [product])      # wrap in a list!
    return HttpResponse(data, content_type="application/json")

def add_product(request):
    formz = forms.ProductForm(request.POST or None)
    if request.method == "POST" and formz.is_valid():
            new_product = formz.save(commit= False)
            new_product.user = request.user
            new_product.save()
            return redirect('main:display')

    return render(request, "upload.html", {'form': formz})    

def buy_product(request, id):
    product = get_object_or_404(models.Product, pk=id)
    product.incr_sold()
    return redirect('main:product_detail', id=id)

@login_required(login_url='/login')
def product_detail(request, id):
    product_details = get_object_or_404(models.Product, pk=id)

    return render(request, "details.html", {
        'product': product_details
    })

@login_required(login_url='/login')
def display(request):
    filter = request.GET.get("filter", "all")

    if filter == "all":
        formz = models.Product.objects.all()
    else:
        formz = models.Product.objects.filter(user = request.user)
    
    return render(request, 'main.html', {
        'name': 'Pulga 10 Store',
        'products': formz,
        'categories': dict(models.Product.choices).values(),
        'account' : request.user.username,
        'last_login': request.COOKIES.get('last_login', 'Never'),
        })
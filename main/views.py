import datetime
from django.shortcuts import render, redirect, get_object_or_404
from main import models
from main import forms
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse("main:login"))
    response.delete_cookie('last_login')
    return response

@csrf_exempt
def delete_product(request, id):
    if request.method == 'POST':
        product = get_object_or_404(models.Product, pk=id)
        product.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid method'}, status=400)

def edit_product(request, id):
    product_detail = get_object_or_404(models.Product, pk=id)
    formz = forms.ProductForm(request.POST or None, instance=product_detail)
    if request.method == "POST" and formz.is_valid():
            formz.save()
            return redirect('main:product_detail', id=id)

    return render(request, "edit.html", {'form': formz})

from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            response = JsonResponse({
                "success": True,
                "redirect_url": reverse("main:display")
            })
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

        else:
            return JsonResponse({
                "success": False,
                "error": "Invalid username or password."
            }, status=400)

    form = AuthenticationForm()
    form.fields['username'].widget.attrs.update({
        'class': 'form-control', 'placeholder': 'Enter username'
    })
    form.fields['password'].widget.attrs.update({
        'class': 'form-control', 'placeholder': 'Enter password'
    })
    return render(request, 'login.html', {'form': form})

@csrf_exempt
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                "success": True,
                "message": "Account successfully created!",
                "redirect_url": reverse("main:login")
            })
        else:
            # Collect form errors to send as JSON
            errors = {field: [str(e) for e in errs] for field, errs in form.errors.items()}
            return JsonResponse({
                "success": False,
                "errors": errors
            }, status=400)

    form = UserCreationForm()
    for field in form.fields.values():
        field.widget.attrs.update({'class': 'form-control'})

    return render(request, 'register.html', {'form': form})

@csrf_exempt
@require_POST
def add_news_entry_ajax(request):
    name = request.POST.get("name")
    description = request.POST.get("description")
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    price = request.POST.get("price")   
    user = request.user

    new_product = models.Product(
        name=name, 
        description=description,
        category=category,
        thumbnail=thumbnail,
        price = price,
        user=user
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)

def show_xml(request):
    products = models.Product.objects.all()
    data = serializers.serialize("xml", products)
    return HttpResponse(data, content_type="application/xml")

def show_json(request):
    try:
        filter_type = request.GET.get("filter", "all").lower()
        user = request.user
        print(f"[DEBUG] filter={filter_type}, user={user}")

        # Filter logic
        if filter_type == "mine":
            products = models.Product.objects.filter(user=user)
        else:
            products = models.Product.objects.all()

        data = []
        for prod in products:
            raw_category = (prod.category or "").strip()
            if not raw_category:
                continue

            # skip lowercase-only categories
            if raw_category.islower():
                continue

            category = raw_category.title()

            # Prevent None user and CharField crash
            owner = prod.user
            username = owner.username if owner else "Unknown"

            data.append({
                "id": str(prod.id),
                "name": prod.name,
                "description": prod.description or "",
                "category": category,
                "thumbnail": prod.thumbnail if prod.thumbnail else "",
                "sold": prod.sold or 0,
                "is_hot": prod.is_hot() if callable(prod.is_hot) else bool(prod.is_hot),
                "username": username,
                "is_owner": (owner == user) if owner else False,
            })

        print(f"[DEBUG] returning {len(data)} products")
        return JsonResponse(data, safe=False)

    except Exception as e:
        print("[ERROR] show_json crashed:")
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)

def xml_by_id(request, id):
    product = get_object_or_404(models.Product, pk=id)
    data = serializers.serialize("xml", [product])
    return HttpResponse(data, content_type="application/xml")

def json_by_id(request, id):
    try:
        product = models.Product.objects.select_related('user').get(pk=id)
        data = {
            'id': str(product.id),
            'name': product.name,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'description': product.description,
            'sold': product.sold,
            'price': product.price,
            'is_hot': product.is_hot(),
            'user_username': product.user.username if product.user else "Unknown",
        }
        return JsonResponse(data)
    except models.Product.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)

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
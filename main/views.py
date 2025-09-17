from django.shortcuts import render, redirect, get_object_or_404
from main import models
from main import forms
from django.http import HttpResponse
from django.core import serializers

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
            formz.save()
            return redirect('main:display')

    return render(request, "upload.html", {'form': formz})    

def product_detail(request, id):
    product_details = get_object_or_404(models.Product, pk=id)

    return render(request, "details.html", {
        'product': product_details
    })

# Create your views here.
def display(request):
    formz = models.Product.objects.all()

    return render(request, 'main.html', {
        'name': 'Pulga 10 Store',
        'nama_saya' : 'Fadhil Daffa Putra Irawan',
        'npm' : '2406438271',
        'products': formz,
        'categories': dict(models.Product.choices).values(),
        })
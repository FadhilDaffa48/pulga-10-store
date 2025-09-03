from django.shortcuts import render

# Create your views here.
def display(request):
    return render(request, 'main.html', {
        'name': 'Pulga 10 Store',
        'nama_saya' : 'Fadhil Daffa Putra Irawan',
        'npm' : '2406438271',
        })
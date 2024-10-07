from django.shortcuts import render

def charts(request):
    return render(request, 'charts.html')

def search(request):
    return render(request, 'search.html')

def about(request):
    return render(request, 'about.html')

def data(request):
    return render(request, 'data.html')
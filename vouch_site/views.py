from django.shortcuts import render

def index(request):
    return render(request, "vouch/index.html")
def search(request):
    return render(request, "vouch/search.html")
def login(request):
    return render(request, "vouch/login.html")

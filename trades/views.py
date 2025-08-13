from django.http import HttpResponse
from django.shortcuts import render
from .utils import internal_salary_audit

def home(request):
    return render(request, "trades/home.html")

def health(request):
    return HttpResponse(internal_salary_audit())

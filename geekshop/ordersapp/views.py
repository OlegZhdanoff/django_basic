from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def orders(request):
    return HttpResponseRedirect(reverse('auth:profile'))


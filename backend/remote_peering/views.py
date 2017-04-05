# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def welcome(request):
    """Just some bogus view to get the server up and running"""
    return HttpResponse("Welcome!")


def api_stub(request):
    """Api stub endpoint"""
    return HttpResponse("Api Welcome!")


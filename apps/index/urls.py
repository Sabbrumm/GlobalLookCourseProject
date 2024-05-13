# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import index_view

urlpatterns = [
    path('', index_view, name="index"),
]

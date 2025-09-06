from django.urls import path
from . import views

urlpatterns = [
    # root path refers to view.index in view.py
    path('', views.index, name="index"), 
    # loans path refers to view.index in view.py
    path('loan/', views.loan, name="loan"), 
    # shows branches for copies by passing <cid> into page
    path('copies/<bid>', views.copybranch, name="copybranch"), 
]
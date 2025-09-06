# define all forms for the app

from django import forms
from django.forms import ModelForm
from .models import Loan

class LoanForm(ModelForm): # Create a venue form
        class Meta: # define the things in the class
            model = Loan # the model imported above ^^^
            fields = "__all__" # if you want all attributes

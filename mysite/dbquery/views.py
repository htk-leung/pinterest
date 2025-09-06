# product-related topics
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.models import Q
from .models import Loan, BookCopy

def index(request):	
	return render(request, 
		'index.html', {})

def loan(request):			    	# set up first function called index to print hello world to screen
	# differentiate between people who just typed the url versus those that clicked search
	if request.method == "POST":
		inputmid = request.POST['inputmid']
		loan_list = Loan.objects.filter(mid__exact=inputmid) 		# grab all records in Loans table
		return render(request, 
			'loan.html', {	
			"loan_list": loan_list,			# pass in library as variable
			"inputmid": inputmid,
		})
	else:
		return render(request, 
			'loan.html', {})
	
def copybranch(request, bid):
	cids = BookCopy.objects.filter(bid__exact=bid).values_list('copyid', flat=True)	
	copies = Loan.objects.filter(Q(copyid__in=cids) & Q(returndate__isnull=False))			    	
	return render(request, 
		'copybranch.html', {	
		"copies": copies,	
	})
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
	# if url includes 'loans/', redirect to loans.urls
	path('', include('dbquery.urls')),
	path('loan/', include('dbquery.urls')), 
	path('admin/', admin.site.urls),
]
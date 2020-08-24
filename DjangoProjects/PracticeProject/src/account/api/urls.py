from django.urls import path

from account.api.views import (
	register_view,
	accountpropertiesview,
	updateaccountview,
	ObtainAuthTokenView,
	)
#from rest_framework.authtoken.views import obtain_auth_token

app_name='account'

urlpatterns=[
	
	path('register/',register_view,name='register'),
	#path('login/',obtain_auth_token,name='login'),
	path('properties/',accountpropertiesview,name='properties'),
	path('properties/update',updateaccountview,name='update'),
	path('login', ObtainAuthTokenView.as_view(), name="login"), 

]
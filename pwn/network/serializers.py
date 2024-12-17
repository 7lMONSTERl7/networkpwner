from rest_framework import serializers
from .models import *

class CommandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ["command"]


class StateSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = State
        fields = ["target", "state", "created"]

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = "__all__"


class VictimsSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Target
        fields = "__all__"
from rest_framework import serializers
from .models import *

class CommandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ["command"]


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = [ "target","command","log"]


class VictimsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = "__all__"
from rest_framework import serializers
from .models import *


class FileSerializer(serializers.ModelSerializer):
    class Meta():
        model = FileManager
        fields = ('file_uploader', 'file_recepient', 'file')

from rest_framework import serializers
from hlr.models import Task


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    status = serializers.CharField(read_only=True, required=False)
    last_update_time = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        model = Task
        fields = ['id', 'author', 'status', 'detail', 'last_update_time']


class TaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['author',  'detail']

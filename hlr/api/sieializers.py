from rest_framework import serializers

from hlr.models import Task, TaskDetail


class ExternalHlrProviderListField(serializers.ListField):
    child = serializers.IntegerField()


class MsisdnListField(serializers.ListField):
    child = serializers.CharField()


class TaskRetrieveSerializer(serializers.ModelSerializer[Task]):
    author = serializers.StringRelatedField()
    status = serializers.CharField(read_only=True, required=False)
    last_update_time = serializers.DateTimeField(read_only=True, required=False)
    # hlr_provider = ExternalHlrProviderListSerializer()

    class Meta:
        model = Task
        fields = ['id', 'author', 'status', 'last_update_time']


class TaskCreateSerializer(serializers.ModelSerializer[Task]):
    external_product_id = ExternalHlrProviderListField()
    msisdn = MsisdnListField()

    class Meta:
        model = Task
        fields = ['id', 'author', 'external_product_id', 'msisdn']


class TaskDetailSerializer(serializers.ModelSerializer[TaskDetail]):

    class Meta:
        model = TaskDetail
        fields = ['id',
                  'task',
                  'external_product_id',
                  'msisdn',
                  'result',
                  'mccmnc',
                  'ported',
                  'message',
                  ]

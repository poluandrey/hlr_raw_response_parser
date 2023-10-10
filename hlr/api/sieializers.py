from rest_framework import serializers

from hlr.models import Task, TaskDetail
from alaris.models import Product


class TaskRetrieveSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    status = serializers.CharField(read_only=True, required=False)
    last_update_time = serializers.DateTimeField(read_only=True, required=False)
    hlr_provider = serializers.SerializerMethodField()

    def get_hlr_provider(self, obj) -> list[str]:
        return Product.objects.filter(alaris_product_id__in=obj)

    class Meta:
        model = Task
        fields = ['id', 'author', 'status', 'hlr_provider', 'msisdn', 'last_update_time', ]


class TaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['author',  'alaris_product_id', 'msisdn', ]


class TaskDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskDetail
        fields = ['id', 'task', 'alaris_product_id', 'msisdn', 'result', 'mcc', 'mnc', 'ported', 'message', ]
from itertools import product

from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework import status

from alaris.models import Product
from hlr.api.sieializers import (TaskCreateSerializer, TaskDetailSerializer,
                                 TaskRetrieveSerializer)
from hlr.models import Task as HlrTask, TaskDetail

from hlr.tasks import celery_task_handler, Task



class TaskView(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin):
    queryset = HlrTask.objects.all()
    serializer_class = TaskRetrieveSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'create':
            return TaskCreateSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = HlrTask.objects.create(author=serializer.validated_data['author'])
        hlr_products = Product.objects.filter(external_product_id__in=serializer.validated_data['external_product_id'])

        for msisdn, hlr_product in product(serializer.validated_data['msisdn'], hlr_products):
            TaskDetail.objects.create(
                task=task,
                external_product_id=hlr_product,
                msisdn=msisdn,
            )
            hlr_task = Task(msisdn=msisdn, provider=hlr_product.description)
            celery_task_handler(task=hlr_task)

        return Response({'id': task.id}, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=True)
    def details(self, request, pk=None):
        task = self.get_object()
        task_detail = task.details.all()
        serializer = TaskDetailSerializer(task_detail, many=True)
        return Response(serializer.data)


class TaskDetailListView(ReadOnlyModelViewSet):
    queryset = TaskDetail.objects.all()
    serializer_class = TaskDetailSerializer

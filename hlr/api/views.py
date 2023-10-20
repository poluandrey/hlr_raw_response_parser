from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from hlr.api.sieializers import (TaskCreateSerializer, TaskDetailSerializer,
                                 TaskRetrieveSerializer)
from hlr.models import Task, TaskDetail


class TaskView(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskRetrieveSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'create':
            return TaskCreateSerializer

        return self.serializer_class

    @action(methods=['get'], detail=True)
    def details(self, request, pk=None):
        task = self.get_object()
        task_detail = task.details.all()
        serializer = TaskDetailSerializer(task_detail, many=True)
        return Response(serializer.data)


class TaskDetailListView(ReadOnlyModelViewSet):
    queryset = TaskDetail.objects.all()
    serializer_class = TaskDetailSerializer

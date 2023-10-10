from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from hlr.models import Task
from hlr.api.sieializers import TaskSerializer, TaskCreateSerializer


class TaskView(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin):
    """
    create HLR task
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'create':
            return TaskCreateSerializer
        return self.serializer_class




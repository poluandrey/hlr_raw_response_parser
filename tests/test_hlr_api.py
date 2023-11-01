import pytest
from hlr.models import Task

from django.urls import reverse


@pytest.mark.django_db
def test__taskview__create_task(client, user, task_create_payload):
    url = reverse('task-list')
    resp = client.post(url, task_create_payload)

    assert resp.status_code == 201
    assert Task.objects.count() == 1

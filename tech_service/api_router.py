from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from hlr.api.views import TaskView, TaskDetailListView
from alaris.api.views import ProductView


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('task', TaskView)
router.register('hlr-request', TaskDetailListView)
router.register('product', ProductView)

appname = 'api'
urlpatterns = router.urls

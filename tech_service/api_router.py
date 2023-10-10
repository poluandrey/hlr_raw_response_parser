from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from alaris.api.views import ProductView
from hlr.api.views import TaskDetailListView, TaskView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('task', TaskView)
router.register('hlr-request', TaskDetailListView)
router.register('product', ProductView)

appname = 'api'
urlpatterns = router.urls

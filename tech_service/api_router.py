from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from hlr.api.views import TaskView


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('task', TaskView)

appname = 'api'
urlpatterns = router.urls

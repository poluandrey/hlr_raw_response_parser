from django.http import HttpResponse
from rest_framework import status


def health_check(request):
    return HttpResponse(status=status.HTTP_200_OK)

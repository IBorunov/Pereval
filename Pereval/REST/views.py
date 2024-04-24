from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView

from REST.models import PerevalAdded
from REST.serializers import PerevalSerializer


class SubmitData(ListCreateAPIView):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalSerializer

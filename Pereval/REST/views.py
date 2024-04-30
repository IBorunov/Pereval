from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from REST.models import PerevalAdded
from REST.serializers import PerevalSerializer


class SubmitData(CreateAPIView):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            response_data = {
                "status": 200,
                "message": "Запись о перевале успешно добавлена.",
                "id": instance.id
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except ValidationError as e:
            response_data = {
                "status": 400,
                "message": "Bad Request. Некорректные данные.",
                "errors": e.detail
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            response_data = {
                "status": 500,
                "message": "Internal Server Error",
                "errors": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RetrievePerevalByID(RetrieveAPIView):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalSerializer


class ListPerevalsByUserEmail(ListAPIView):
    serializer_class = PerevalSerializer

    def get_queryset(self):
        email = self.request.query_params.get('user__email', '')
        return PerevalAdded.objects.filter(user__email=email)


class UpdatePereval(APIView):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalSerializer

    def patch(self, request, *args, **kwargs):
        instance = PerevalAdded.objects.get(pk=kwargs['pk'])

        if instance.status != 'new':
            return Response({"state": 0, "message": "Невозможно редактировать запись."}, status=400)

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"state": 1}, status=200)
        return Response({"state": 0, "message": serializer.errors}, status=400)
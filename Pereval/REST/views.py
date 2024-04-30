from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response

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


class UpdatePereval(UpdateAPIView):
    queryset = PerevalAdded.objects.filter(status='new')
    serializer_class = PerevalSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        protected_fields = ['fam', 'name', 'otc', 'email', 'phone']

        #проверяем, есть ли у нас в запросе защищенные поля
        for field in protected_fields:
            if field in data:
                #удаляем эти поля из request.data и обрабатываем запрос уже без этих данных
                data.pop(field)

        serializer = self.serializer_class(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"state": 1}, status=200)
        return JsonResponse({"state": 0, "message": "Невозможно обновить запись."}, status=400)
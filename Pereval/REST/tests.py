from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
from .serializers import PerevalSerializer
from .models import User, PerevalAdded, Coord, Level, Image
import requests

class PassTestCase(APITestCase):

    def setUp(self):
        # Объект перевал 1
        self.pass_1 = PerevalAdded.objects.create(
            user=User.objects.create(
                email='Ivanov@mail.ru',
                fam='Иванов',
                name = 'Петр',
                otc = 'Васильевич',
                phone='89999999999'
            ),
            beauty_title='beauty_title',
            title='title',
            other_titles='other_title',
            connect='connect',
            coords=Coord.objects.create(
                latitude=22.222,
                longitude=11.111,
                height=1000
            ),
            level=Level.objects.create(
                winter='1A',
                summer='1A',
                autumn='1A',
                spring='1A'
            )
        )

        # Изображение для объекта перевал 1
        self.image_1 = Image.objects.create(
            title='Title_1',
            data='https://images.gl/eTdfdfgk33vNQG8',
            pereval=self.pass_1
        )

        # Объект перевал 2
        self.pass_2 = PerevalAdded.objects.create(
            user=User.objects.create(
                email='Petrov@mail.ru',
                fam='Петров',
                name='Иван',
                otc='Васильевич',
                phone='89999998877'
            ),
            beauty_title='beauty_title2',
            title='title2',
            other_titles='other_title2',
            connect='connect2',
            coords=Coord.objects.create(
                latitude=11.222,
                longitude=22.111,
                height=2000
            ),
            level=Level.objects.create(
                winter='1A',
                summer='1A',
                autumn='1A',
                spring='1A'
            )
        )

        # Изображение для объекта перевал 2
        self.image_2 = Image.objects.create(
            title='Title_2',
            data='https://images.gl/8JQjhxTuFYCcRG7',
            pereval=self.pass_2
        )

    def test_pereval_user_email(self):

        email = self.pass_1.user.email
        url = f'/api/v1/getlist/?user__email={email}'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_SubmitData(self):
        url = '/api/v1/submitdata'

        data = {
            "beauty_title": "Перевал",
            "title": "Пхия",
            "other_titles": "Триев",
            "connect": "тест",
            "add_time": "2021-09-22 13:18:13",
            "user": {"email": "test5@gmail.com",
                     "fam": "Пупкин",
                     "name": "Василий",
                     "otc": "Васильевич",
                     "phone": "+7 555 55 55"},

            "coords": {
                "latitude": "45.3842",
                "longitude": "7.1525",
                "height": "1200"},

            "level": {"winter": "3Б",
                      "summer": "2Б",
                      "autumn": "1Б",
                      "spring": "1Б"},

            "images": [
                {"data": "https://pibig.info/uploads/posts/2022-11/1669750047_4-pibig-info-p-pkhiya-krasivo-5.jpg",
                 "title": "Седловина"}]
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_RetrievePerevalByID(self):
        url = reverse('retrieve_pereval_by_id', kwargs={'pk': self.pass_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_UpdatePereval(self):
        url = reverse('update_pereval', kwargs={'pk': self.pass_2.id})
        data = {
            "beauty_title": "Перевал",
            "title": "Пхия",
            "other_titles": "Триев",
            "connect": "тест",
            "add_time": "2021-09-22 13:18:13",
            "user": {"email": "Petrov@mail.ru",
                     "fam": "Петров",
                     "name": "Иван",
                     "otc": "Васильевич",
                     "phone": "89999998877"},

            "coords": {
                "latitude": "45.3842",
                "longitude": "7.1525",
                "height": "1200"},

            "level": {"winter": "3Б",
                      "summer": "2Б",
                      "autumn": "1Б",
                      "spring": "1Б"},

            "images": [
                {"data": "https://pibig.info/uploads/posts/2022-11/1669750047_4-pibig-info-p-pkhiya-krasivo-5.jpg",
                 "title": "Седловина"}]
        }
        response = self.client.patch(url, data=data)
        if response.status_code != 200:
            print(f'An error occurred. Server response code: {response.status_code}')
            print('Response content:')
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
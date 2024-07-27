from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Users, Pereval, Coords, Level, Images

class UsersModelTest(TestCase):

    def setUp(self):
        self.user = Users.objects.create(
            email='john.doe@example.com',
            fam='Doe',
            name='John',
            pat='Michael',
            phone='1234567890'
        )

    def test_user_creation(self):
        user = Users.objects.get(email='john.doe@example.com')
        self.assertEqual(user.fam, 'Doe')
        self.assertEqual(user.name, 'John')
        self.assertEqual(user.pat, 'Michael')
        self.assertEqual(user.phone, '1234567890')


class PerevalModelTest(APITestCase):

    def setUp(self):
        self.user = Users.objects.create(
            email='testuser@example.com',
            fam='Doe',
            name='John',
            pat='Michael',
            phone='1234567890'
        )
        self.level = Level.objects.create(
            winter_lev='4A',
            spring_lev='2A',
            summer_lev='1A',
            autumn_lev='3A'
        )
        self.coord = Coords.objects.create(latitude=0.0, longitude=0.0, height=1000)

        self.pereval = Pereval.objects.create(
            beauty_title='Mountain',
            title='Everest',
            other_titles='Peak',
            connect='Via Nepal',
            coord=self.coord,
            user=self.user,
            level=self.level
        )

    def test_pereval_creation(self):
        self.assertTrue(Pereval.objects.exists())


class CoordsModelTest(TestCase):

    def setUp(self):
        self.coords = Coords.objects.create(
            latitude=45.0,
            longitude=90.0,
            height=2000
        )

    def test_coords_creation(self):
        coords = Coords.objects.get(latitude=45.0, longitude=90.0)
        self.assertEqual(coords.height, 2000)

    def test_str_representation(self):
        self.assertEqual(str(self.coords), f'Широта: {self.coords.latitude} Долгота: {self.coords.longitude} Высота: {self.coords.height}')


class LevelModelTest(TestCase):

    def setUp(self):
        self.level = Level.objects.create(
            winter_lev='4A',
            spring_lev='2A',
            summer_lev='1A',
            autumn_lev='3A'
        )

    def test_level_creation(self):
        level = Level.objects.get(winter_lev='4A')
        self.assertEqual(level.spring_lev, '2A')

    def test_str_representation(self):
        self.assertEqual(
            str(self.level),
            f'Весна:{self.level.spring_lev} Лето:{self.level.summer_lev} Осень:{self.level.autumn_lev} Зима:{self.level.winter_lev}'
        )


class ImagesModelTest(TestCase):

    def setUp(self):
        self.coords = Coords.objects.create(
            latitude=45.0,
            longitude=90.0,
            height=2000
        )
        self.user = Users.objects.create(
            email='john.doe@example.com',
            fam='Doe',
            name='John',
            pat='Michael',
            phone='1234567890'
        )
        self.level = Level.objects.create(
            winter_lev='4A',
            spring_lev='2A',
            summer_lev='1A',
            autumn_lev='3A'
        )
        self.pereval = Pereval.objects.create(
            beauty_title='Test Peak',
            title='Peak Test',
            other_titles='Test',
            connect='Test Connection',
            coord=self.coords,
            user=self.user,
            status=Pereval.NEW,
            level=self.level
        )
        self.image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.image = Images.objects.create(
            image=self.image_file,
            title='Test Image',
            pereval_id=self.pereval
        )

    def test_image_creation(self):
        image = Images.objects.get(title='Test Image')
        self.assertEqual(image.pereval_id, self.pereval)


class PerevalAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = Users.objects.create(
            email='test@example.com',
            fam='Doe',
            name='John',
            pat='Michael',
            phone='1234567890'
        )
        self.level = Level.objects.create(
            winter_lev='4A',
            spring_lev='2A',
            summer_lev='1A',
            autumn_lev='3A'
        )
        self.coord = Coords.objects.create(latitude=0.0, longitude=0.0, height=1000)

        self.pereval = Pereval.objects.create(
            beauty_title='Test Beauty Title',
            title='Test Title',
            other_titles='Other Title',
            connect='Test Connect',
            user=self.user,
            coord=self.coord,
            level=self.level,
        )

    def test_create_pereval(self):
        response = self.client.post(reverse('perevals-list'), {
            'beauty_title': 'New Title',
            'title': 'New Pereval',
            'other_titles': 'New Other Title',
            'connect': 'New Connect',
            'user': self.user.id,
            'coord': self.coord.id,
            'level': self.level.id,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

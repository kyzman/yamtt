from django.test import TestCase
from menu.models import Menu
from django.db.utils import IntegrityError

# Create your tests here.


class TestMenuModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        Menu.objects.create(title='some_menu')

    def test_valid_constraint(self):
        menu = Menu.objects.get(title='some_menu')
        self.assertIsNotNone(menu)

    def test_invalid_cyr_constraint(self):
        with self.assertRaises(IntegrityError):
            new = Menu.objects.create(title='Меню')

    def test_valid_cyr_constraint(self):
        menu = Menu.objects.get(title='some_menu')
        new_item = Menu.objects.create(title='Меню', parent=menu)
        self.assertIsNotNone(new_item)

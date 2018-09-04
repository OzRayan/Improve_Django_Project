from django.contrib.auth.models import User
from django.test import TestCase

from .models import Menu, Item, Ingredient

import datetime


class BaseTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='tomika',
            email='example@mail.com',
            password='tomika'
        )
        # noinspection PyUnresolvedReferences
        self.ingredient_1 = Ingredient.objects.create(name='salt')
        # noinspection PyUnresolvedReferences
        self.ingredient_2 = Ingredient.objects.create(name='pepper')
        # noinspection PyUnresolvedReferences
        self.item_1 = Item.objects.create(
            name='Soup',
            description='Chicken soup',
            standard=False,
            chef=self.user
        )
        # noinspection PyUnresolvedReferences
        self.item_2 = Item.objects.create(
            name='Gordon bleu',
            description='Chesse wrapped meat',
            standard=True,
            chef=self.user
        )
        self.item_1.set([self.ingredient_1, self.ingredient_2])
        self.item_2.set([self.ingredient_1, self.ingredient_2])

        # noinspection PyUnresolvedReferences
        self.menu_1 = Menu.objects.create(
            season='Fall',
            expiration_date=datetime.date.today()
        )
        # noinspection PyUnresolvedReferences
        self.menu_2 = Menu.objectss.create(
            season='Winter',
            expiration_date=datetime.date.today()
        )

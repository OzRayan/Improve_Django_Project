from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse

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
        self.item_1.ingredients.add(self.ingredient_1)
        self.item_2.ingredients.set([self.ingredient_1, self.ingredient_2])

        # noinspection PyUnresolvedReferences
        self.menu_1 = Menu.objects.create(
            season='Summer',
            expiration_date=datetime.date.today()
        )
        # noinspection PyUnresolvedReferences
        self.menu_2 = Menu.objects.create(
            season='Winter',
            expiration_date=datetime.date.today()
        )
        self.menu_1.items.add(self.item_1)
        self.menu_2.items.set([self.item_1, self.item_2])


class MenuTest(BaseTest):

    def test_menu_list_view(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')
        # noinspection PyUnresolvedReferences
        self.assertEqual(len(Menu.objects.all()), 2)

    def test_menu_detail_view(self):
        resp = self.client.get(reverse('menu:menu_detail',
                               kwargs={'pk': self.menu_1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')
        self.assertContains(resp, self.item_1.name)
        self.assertContains(resp, self.menu_1.season)

    def test_create_new_menu_view(self):
        resp = self.client.get(reverse('menu:menu_new'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/add_menu.html')

        # With form
        data = {
            'season': 'Summer',
            'items': [self.item_1.id, self.item_2.id],
            'expiration_date': datetime.date.today()
        }
        resp_2 = self.client.post('/menu/new/', data)
        # noinspection PyUnresolvedReferences
        menu = Menu.objects.all().order_by('-id')[0]
        self.assertEqual(resp_2.status_code, 302)
        self.assertRedirects(resp_2, reverse('menu:menu_detail',
                                             kwargs={'pk': menu.id}))

    def test_edit_menu_view(self):
        resp = self.client.get(reverse('menu:menu_edit',
                                       kwargs={'pk': self.menu_1.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/add_menu.html')

        # With form
        data = {
            'season': 'Now this is Fall',
            'items': [self.item_2.id],
            'expiration_date': datetime.date.today()
        }
        # noinspection PyUnresolvedReferences
        menu = Menu.objects.all().order_by('-id')[0]
        resp_2 = self.client.post(reverse('menu:menu_edit',
                                  kwargs={'pk': menu.id}), data)
        self.assertEqual(resp_2.status_code, 302)

    def test_delete_menu_view(self):
        resp = self.client.get(reverse('menu:menu_delete',
                                       kwargs={'pk': self.menu_1.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/delete_menu.html')

        resp_2 = self.client.post(reverse('menu:menu_delete',
                                          kwargs={'pk': self.menu_1.id}))
        # noinspection PyUnresolvedReferences
        self.assertEqual(len(Menu.objects.all()), 1)
        self.assertRedirects(resp_2, reverse('menu:menu_list'))


class ItemTest(BaseTest):

    def test_item_list_view(self):
        resp = self.client.get('/menu/items/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/item_list.html')
        # noinspection PyUnresolvedReferences
        self.assertEqual(len(Item.objects.all()), 2)

    def test_item_detail_view(self):
        resp = self.client.get(reverse('menu:item_detail',
                                       kwargs={'pk': self.item_1.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/detail_item.html')
        self.assertContains(resp, self.ingredient_1.name)
        self.assertContains(resp, self.item_1.name)

    def test_create_new_item_view(self):
        resp = self.client.get(reverse('menu:item_new'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/edit_item.html')

        data = {
            'name': 'Soup',
            'description': 'Tomato soup',
            'chef': self.user,
            'ingredients': [self.ingredient_1.id, self.ingredient_2.id],
            'standard': True
        }
        resp_2 = self.client.post('/menu/item/new/', data)
        self.assertEqual(resp_2.status_code, 200)

    def test_edit_item_view(self):
        resp = self.client.get(reverse('menu:item_edit',
                                       kwargs={'pk': self.item_1.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/edit_item.html')

        # With form
        data = {
            'name': 'Soup',
            'description': 'Chiken soup',
            'chef': self.user,
            'ingredients': [self.ingredient_1.id, self.ingredient_2.id],
            'standard': True
        }

        resp_2 = self.client.post(reverse('menu:item_edit',
                                  kwargs={'pk': self.item_1.id}), data)
        # noinspection PyUnresolvedReferences
        item = Item.objects.all().order_by('-id')[0]
        self.assertEqual(resp_2.status_code, 200)

    def test_delete_item_view(self):
        resp = self.client.get(reverse('menu:item_delete',
                                       kwargs={'pk': self.item_1.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/delete_item.html')

        resp_2 = self.client.post(reverse('menu:item_delete',
                                          kwargs={'pk': self.item_1.id}))
        # noinspection PyUnresolvedReferences
        self.assertEqual(len(Item.objects.all()), 1)
        self.assertEqual(resp_2.status_code, 302)
        self.assertRedirects(resp_2, '/menu/items/')

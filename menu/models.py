from django.db import models
from django.utils import timezone


class Menu(models.Model):
    """Menu model class
    Inherit: - models.Model
    fields: - season: - CharField
            - items: ManyToManyField
            -created_date: DateTimeField
            -expiration_date: DateField
    """
    season = models.CharField(max_length=20)
    items = models.ManyToManyField('Item', related_name='items')
    created_date = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateField(help_text='MM/DD/YYYY',
                                       blank=True, null=True)

    def __str__(self):
        """Returns season field name"""
        return self.season


class Item(models.Model):
    """Item model class
    Inherit: -models.Model
    fields: - name: - CharField
            - description: - TextField
            - chef: - ForeignKey
            - standard: - BooleanField
            - ingredients: - ManyToManyField
    """
    name = models.CharField(max_length=20)
    description = models.TextField()
    chef = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(
        'Ingredient', related_name='ingredients')

    def __str__(self):
        """Returns name field name"""
        return self.name


class Ingredient(models.Model):
    """Ingredient model class
    Inherit: - models.Model
    field: - name: - CharField
    """
    name = models.CharField(max_length=20)

    def __str__(self):
        """Return name field name"""
        return self.name

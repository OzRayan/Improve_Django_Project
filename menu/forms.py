from django.forms import DateField, ModelForm, ValidationError
from django.forms.extras.widgets import SelectDateWidget
from django.utils import timezone
import datetime

from .models import Menu, Item, Ingredient


class MenuForm(ModelForm):
    class Meta:
        model = Menu
        exclude = ('created_date',)

    def clean(self):
        cleaned_data = super(MenuForm, self).clean()
        items = cleaned_data.get('items')
        expiration_date = cleaned_data.get('expiration_date')

        if expiration_date:
            if expiration_date < datetime.date.today():
                raise ValidationError('Expiration date already passed!!')
        if items:
            if len(items) < 1:
                raise ValidationError("You must select one or more items!")
        else:
            raise ValidationError('You must select one or more items!')

        return cleaned_data


class ItemForm(ModelForm):

    class Meta:
        model = Item
        exclude = ('created_date',)

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get('description')
        ingredients = cleaned_data.get('ingredients')
        if not description or len(description) < 10:
            raise ValidationError('Description must contain at least 10 characters!')
        if ingredients:
            if len(ingredients) < 2:
                raise ValidationError('You must select two or more ingredients!')

        return cleaned_data

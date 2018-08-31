from django.forms import ModelForm, ValidationError
from django.forms.extras.widgets import SelectDateWidget

from .models import Menu, Item, Ingredient


class MenuForm(ModelForm):

    class Meta:
        model = Menu
        exclude = ('created_date',)

    def clean_items(self):
        data = self.cleaned_data.get('items')
        if len(data) <= 3:
            raise ValidationError("Must select four or more items")
        return data

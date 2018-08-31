from django.forms import ModelForm, ValidationError
from django.forms.extras.widgets import SelectDateWidget
from django.utils import timezone

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
            if expiration_date <= timezone.now():
                raise ValidationError('Expiration date already passed!!')
        if items:
            if len(items) <= 3:
                raise ValidationError("You must select four or more items!")
        else:
            raise ValidationError('You must select four or more items!')

        return cleaned_data

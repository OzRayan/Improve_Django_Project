from django.forms import DateField, ModelForm, ValidationError, SelectDateWidget

from .models import Menu, Item

import datetime


class MenuForm(ModelForm):
    """MenuForm class
    Inherit: - ModelForm
    field: - expiration_date: - DateField with SelectDateWidget and range of years for selection
    """
    year = datetime.datetime.today().year
    year_range = tuple([i for i in range(year, year + 3)])
    expiration_date = DateField(
        required=False, widget=SelectDateWidget(years=year_range)
    )

    class Meta:
        model = Menu
        exclude = ('created_date',)

    def clean(self):
        """clean method, overrides the super class clean() method.
        - Makes sure expiration date is not passed if there is one.
        - Makes sure that at least 1 item is selected.
        -:return: - cleaned_data
        """
        cleaned_data = super().clean()
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
    """ItemForm class
    Inherit: - ModelForm
    """

    class Meta:
        model = Item
        exclude = ('created_date',)

    def clean(self):
        """clean method, overrides the super class clean() method.
        - Makes sure that description has at least 10 characters in it.
        - Makes sure that at least 2 ingredients is selected.
        -:return: - cleaned_data
        """
        cleaned_data = super().clean()
        description = cleaned_data.get('description')
        ingredients = cleaned_data.get('ingredients')
        if not description or len(description) < 10:
            raise ValidationError('Description must contain at least 10 characters!')
        if ingredients:
            if len(ingredients) < 2:
                raise ValidationError('You must select two or more ingredients!')

        return cleaned_data

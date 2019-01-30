from django.shortcuts import get_object_or_404, redirect, render

from .models import Menu, Item
from .forms import MenuForm, ItemForm

from operator import attrgetter
import datetime


def menu_list(request):
    """Menu list view, selects all the menu objects related to 'items'
    :return: - list_all_current.html + menu_list with expiration date
                                     + menu_list without expiration date
    """
    # noinspection PyUnresolvedReferences
    all_menus = Menu.objects.all().prefetch_related('items')
    menus_no_expdate = []  # all_menus.exclude(expiration_date__gt=datetime.date.today())

    menus = []  # all_menus.filter(expiration_date__gt=datetime.date.today())
    for menu in all_menus:
        if menu.expiration_date:
            if menu.expiration_date > datetime.date.today():
                menus.append(menu)
        else:
            menus_no_expdate.append(menu)
    # Sorts menus by expiration date
    menus = sorted(menus, key=attrgetter('created_date'))[::-1]
    # Sorts menus_no_expdate by season
    menus_no_expdate = sorted(menus_no_expdate, key=attrgetter('season'))
    return render(request, 'menu/list_all_current_menus.html',
                  {'menus': menus,
                   'no_date': menus_no_expdate})


def menu_detail(request, pk):
    """Menu detail view - get menu object 'pk'
    :input: - pk - menu id
    :return: - menu_detail.html + dictionary of menu values
    """
    menu = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def create_new_menu(request):
    """Create new menu view
    :return: - add_menu.html + form for new menu
    """
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()
            return redirect('menu:menu_detail', pk=menu.pk)
    return render(request, 'menu/add_menu.html', {'form': form})


def edit_menu(request, pk):
    """Edit menu view - get menu object by 'pk'
    :input: - pk - menu id
    :return: - add_menu.html + form for new menu
    """
    menu = get_object_or_404(Menu, pk=pk)
    form = MenuForm(instance=menu)
    if request.method == "POST":
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            menu_data = form.save()
            return redirect('menu:menu_detail', pk=menu_data.pk)
    return render(request, 'menu/add_menu.html', {'form': form, 'key': True})


def delete_menu(request, pk):
    """Delete menu view - get menu object by 'pk'
    :input: - pk - menu id
    :return: - redirect to menu_list
             - delete_menu.html + menu dictionary with values
    """
    menu_d = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        menu_d.delete()
        return redirect('menu:menu_list')
    return render(
        request, 'menu/delete_menu.html', {'menu': menu_d})


def item_list(request):
    """Item list view, selects all the item objects
    :return: - item_list.html + item list dictionary
    """
    # noinspection PyUnresolvedReferences
    items = Item.objects.all()
    # Sorts items by alphabet
    items = sorted(items, key=attrgetter('name'))

    return render(request, 'menu/item_list.html', {'items': items})


def item_detail(request, pk):
    """Item detail view - get item object 'pk'
    :input: - pk - item id
    :return: - detail_item.html + dictionary of item values
    """
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_item(request):
    """Create new item view
    :return: - edit_item.html + form for new item
    """
    form = ItemForm()
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            return redirect('menu:item_detail', pk=item.pk)
    return render(request, 'menu/edit_item.html', {'form': form})


def edit_item(request, pk):
    """Edit item view - get item object by 'pk'
    :input: - pk - item id
    :return: - edit_item.html + form for item
    """
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            item_data = form.save()
            return redirect('menu:item_detail', pk=item_data.pk)
    else:
        form = ItemForm(instance=item)
    return render(request, 'menu/edit_item.html', {'form': form, 'key': True})


def delete_item(request, pk):
    """Delete item view - get item object by 'pk'
    :input: - pk - item id
    :return: - redirect to item_list
             - delete_item.html + item dictionary with values
    """
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('menu:item_list')
    return render(request, 'menu/delete_item.html', {'item': item})

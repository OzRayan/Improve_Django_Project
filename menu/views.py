from django.shortcuts import get_object_or_404, redirect, render
from operator import attrgetter

from .models import *
from .forms import *


def menu_list(request):
    """Menu list view, selects all the menu objects related to 'items'
    :return: - list_all_current.html + menu_list with expiration date
                                     + menu_list without expiration date
    """
    # noinspection PyUnresolvedReferences
    all_menus = Menu.objects.all().prefetch_related('items')
    menus_no_expdate = []
    menus = []
    for menu in all_menus:
        if menu.expiration_date:
            if menu.expiration_date >= timezone.now():
                menus.append(menu)
        else:
            menus_no_expdate.append(menu)
    # Sorts menus by expiration date
    menus = sorted(menus, key=attrgetter('expiration_date'))
    # Sorts menus_no_expdate by season
    menus_no_expdate = sorted(menus_no_expdate, key=attrgetter('season'))
    return render(request, 'menu/list_all_current_menus.html',
                  {'menus': menus, 'no_date': menus_no_expdate})


def menu_detail(request, pk):
    """Menu detail view - get menu object 'pk'
    :input: - pk - menu id
    :return: - menu_detail.html + dictionary of menu values
    """
    menu = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    """Item detail view - get item object 'pk'
    :input: - pk - item id
    :return: - detail_item.html + dictionary of item values
    """
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'menu/detail_item.html', {'item': item})


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
            menu = form.save()
            return redirect('menu:menu_detail', pk=menu.pk)
    return render(request, 'menu/add_menu.html', {'form': form})


def delete_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        menu.delete()
        return redirect('menu_list')
    return render(
        request, 'menu/menu_delete.html', {'menu': menu}
    )

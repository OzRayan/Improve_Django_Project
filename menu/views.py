from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from operator import attrgetter
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *


def menu_list(request):
    all_menus = Menu.objects.all().prefetch_related('items')
    menus_no_expdate = []
    menus = []
    for menu in all_menus:
        if menu.expiration_date:
            if menu.expiration_date >= timezone.now():
                menus.append(menu)
        else:
            menus_no_expdate.append(menu)
    menus = sorted(menus, key=attrgetter('expiration_date'))
    menus_no_expdate = sorted(menus_no_expdate, key=attrgetter('season'))
    return render(request, 'menu/list_all_current_menus.html',
                  {'menus': menus, 'no_date': menus_no_expdate})


def menu_detail(request, pk):
    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    try: 
        item = Item.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()
            return redirect('menu:menu_detail', pk=menu.pk)
    return render(request, 'menu/add_menu.html', {'form': form})


def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    items = Item.objects.all()
    if request.method == "POST":
        menu.season = request.POST.get('season', '')
        menu.expiration_date = datetime.strptime(request.POST.get('expiration_date', ''), '%m/%d/%Y')
        menu.items = request.POST.get('items', '')
        menu.save()

    return render(request, 'menu/change_menu.html', {
        'menu': menu,
        'items': items,
        })

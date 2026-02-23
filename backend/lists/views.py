from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ShoppingList, Item
from .tasks import categorize_item_task

@login_required
def dashboard(request):
    user_group = request.user.family_group
    if user_group:
        lists = ShoppingList.objects.filter(family_group=user_group)
    else:
        lists = ShoppingList.objects.none()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if name and user_group:
            ShoppingList.objects.create(
                name=name,
                family_group=user_group,
                created_by=request.user
            )
            return redirect('dashboard')

    return render(request, 'lists/dashboard.html', {'lists': lists})

@login_required
def list_detail(request, pk):
    shopping_list = get_object_or_404(ShoppingList, pk=pk, family_group=request.user.family_group)
    items = shopping_list.items.all().order_by('category__name', 'created_at')
    
    # Render full page or just partial if it's HTMX request
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'lists/partials/item_list.html', {'shopping_list': shopping_list, 'items': items})
    
    return render(request, 'lists/list_detail.html', {'shopping_list': shopping_list, 'items': items})

@login_required
def add_item(request, pk):
    shopping_list = get_object_or_404(ShoppingList, pk=pk, family_group=request.user.family_group)
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        
        if name:
            item = Item.objects.create(
                shopping_list=shopping_list,
                name=name,
                quantity=quantity,
                added_by=request.user
            )
            # Aciona a categorização
            categorize_item_task.delay(item.id)
            
            # Retorna apenas o HTML do novo item
            return render(request, 'lists/partials/item_row.html', {'item': item})
    
    return redirect('list_detail', pk=pk)

@login_required
def toggle_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id, shopping_list__family_group=request.user.family_group)
    if request.method == 'POST':
        item.is_checked = not item.is_checked
        item.save()
        return render(request, 'lists/partials/item_row.html', {'item': item})
    
    return redirect('list_detail', pk=item.shopping_list.id)
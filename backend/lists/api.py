from ninja import Router
from django.shortcuts import get_object_or_404
from .models import ShoppingList, Item
from .schemas import ShoppingListSchema, ItemSchema, ItemCreateSchema, ItemUpdateSchema
from typing import List

lists_router = Router(tags=["Lists"])
items_router = Router(tags=["Items"])

@lists_router.get("/", response=List[ShoppingListSchema])
def list_shopping_lists(request):
    # Por enquanto retornamos as listas cujo grupo familiar o usuário pertence.
    # Assumindo que o usuário tem um family_group atribuído, senão retorna vazio.
    if request.user.is_authenticated and request.user.family_group:
        return ShoppingList.objects.filter(family_group=request.user.family_group)
    # Fallback para desenvolvimento: retorna todas as listas se não houver grupo
    return ShoppingList.objects.all()

@lists_router.post("/{list_id}/items", response=ItemSchema)
def create_item(request, list_id: int, payload: ItemCreateSchema):
    shopping_list = get_object_or_404(ShoppingList, id=list_id)
    user = request.user if request.user.is_authenticated else None
    
    item = Item.objects.create(
        shopping_list=shopping_list,
        name=payload.name,
        quantity=payload.quantity,
        added_by=user
    )
    return item

@items_router.patch("/{item_id}", response=ItemSchema)
def update_item_status(request, item_id: int, payload: ItemUpdateSchema):
    item = get_object_or_404(Item, id=item_id)
    item.is_checked = payload.is_checked
    item.save()
    return item

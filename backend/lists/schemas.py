from ninja import Schema, ModelSchema
from .models import ShoppingList, Item, Category
from typing import Optional, List

class CategorySchema(ModelSchema):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon']

class ItemSchema(ModelSchema):
    category: Optional[CategorySchema] = None

    class Meta:
        model = Item
        fields = ['id', 'name', 'quantity', 'is_checked', 'created_at']

class ShoppingListSchema(ModelSchema):
    items: List[ItemSchema] = []

    class Meta:
        model = ShoppingList
        fields = ['id', 'name', 'created_at']

    @staticmethod
    def resolve_items(obj):
        return obj.items.all()

class ItemCreateSchema(Schema):
    name: str
    quantity: Optional[str] = None

class ItemUpdateSchema(Schema):
    is_checked: bool

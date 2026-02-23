from ninja import NinjaAPI
from lists.api import lists_router, items_router

api = NinjaAPI(title="TrazAí API", version="1.0.0")

api.add_router("/lists", lists_router)
api.add_router("/items", items_router)

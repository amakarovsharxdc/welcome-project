from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import JSONResponse

from .models import Items


router = APIRouter()


@router.post('/items.json', response_class=JSONResponse)
def post_items(request: Request, items: Items):
    request.app.api.add_items(items)
    return request.app.api.get_tree()

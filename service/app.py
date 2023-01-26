from fastapi import FastAPI

from .api import API
from .handlers import router
from .storage import Storage


app = FastAPI()
app.api = API(Storage())
app.include_router(router)

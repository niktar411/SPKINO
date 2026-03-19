from src.backend.routes.cruds import router as crud_router
from src.backend.routes.pages import router as page_router
from fastapi import APIRouter
routers = []

for k, v in list(globals().items()):
    cond1 = '_router' in k
    cond2 = isinstance(v, APIRouter)
    if cond1 and cond2:
        routers.append(v)


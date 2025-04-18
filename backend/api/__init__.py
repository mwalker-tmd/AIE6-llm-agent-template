from fastapi import APIRouter
from .upload import router as upload_router
from .query import router as query_router

router = APIRouter()
router.include_router(upload_router, tags=["upload"])
router.include_router(query_router, tags=["query"]) 
from fastapi import APIRouter

from app.models.schema import SearchRequest

router = APIRouter()

@router.post("/search")
def search(request: SearchRequest):
    return{
        "received_query": request.query
    }

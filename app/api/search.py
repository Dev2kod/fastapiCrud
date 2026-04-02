from fastapi import APIRouter
from app.models.schema import SearchRequest
from app.core.queryParser import parseQuery
router = APIRouter()


@router.post("/search")
def search(request: SearchRequest):
    print(request)
    parsedQuery = parseQuery(request.query)
    return{
        "parsed": parsedQuery
    }

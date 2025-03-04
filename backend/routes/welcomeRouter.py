from fastapi import APIRouter

router = APIRouter()


@router.get("/hello")
def search(query: str):
    return {"results": "hello world"}

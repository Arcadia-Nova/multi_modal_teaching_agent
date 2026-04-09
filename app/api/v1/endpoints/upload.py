from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
async def test_upload():
    return {"message": "Upload endpoint is active"}

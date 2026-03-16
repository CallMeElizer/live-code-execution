from fastapi import APIRouter
from app.worker import execute_code
from app.schemas import SessionCreate, CodeUpdate

router = APIRouter()

@router.post("/code-sessions/{sesson_id}/run")
async def run_code(sesson_id: str):
    task = execute_code.delay(execute_id="uuid", language="python", code="print('Hello, World!')")
    return {"task_id": task.id, "status": "QUEUED"}